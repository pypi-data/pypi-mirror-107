"""This is the TreeView that is most common (for example: it is used in
Rational Rose).

This is a tree based on namespace relationships. As a result only
classifiers are shown here.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Optional, Set

from gi.repository import Gdk, Gio, GLib, Gtk

from gaphor import UML
from gaphor.core import action, event_handler, gettext, transactional
from gaphor.core.modeling import Diagram, Element, Presentation
from gaphor.ui.abc import UIComponent
from gaphor.ui.actiongroup import create_action_group
from gaphor.ui.event import DiagramOpened, DiagramSelectionChanged
from gaphor.ui.namespacemodel import (
    RELATIONSHIPS,
    NamespaceModel,
    NamespaceModelElementDropped,
    NamespaceModelRefreshed,
)
from gaphor.ui.namespaceview import namespace_view

if TYPE_CHECKING:
    from gaphor.core.eventmanager import EventManager
    from gaphor.core.modeling import ElementFactory


log = logging.getLogger(__name__)


def popup_model(element):
    model = Gio.Menu.new()

    part = Gio.Menu.new()
    part.append(gettext("_Open"), "tree-view.open")
    part.append(gettext("_Rename"), "tree-view.rename")
    model.append_section(None, part)

    part = Gio.Menu.new()
    part.append(gettext("New _Diagram"), "tree-view.create-diagram")
    part.append(gettext("New _Package"), "tree-view.create-package")
    model.append_section(None, part)

    part = Gio.Menu.new()
    part.append(gettext("De_lete"), "tree-view.delete")
    model.append_section(None, part)

    if not element:
        return model

    part = Gio.Menu.new()
    for presentation in element.presentation:
        diagram = presentation.diagram
        if diagram:
            menu_item = Gio.MenuItem.new(
                gettext('Show in "{diagram}"').format(diagram=diagram.name),
                "tree-view.show-in-diagram",
            )
            menu_item.set_attribute_value("target", GLib.Variant.new_string(diagram.id))
            part.append_item(menu_item)

        # Play it safe with an (arbitrary) upper bound
        if part.get_n_items() > 29:
            break

    if part.get_n_items() > 0:
        model.append_section(None, part)
    return model


class Namespace(UIComponent):
    def __init__(self, event_manager: EventManager, element_factory: ElementFactory):
        self.event_manager = event_manager
        self.element_factory = element_factory

        self.model: Optional[NamespaceModel] = None
        self.view: Optional[Gtk.TreeView] = None
        self.scrolled_window: Optional[Gtk.ScrolledWindow] = None
        self.ctrl: Set[Gtk.EventController] = set()

    def open(self):
        self.model = NamespaceModel(self.event_manager, self.element_factory)
        view = namespace_view(self.model)
        self.event_manager.subscribe(self._on_model_refreshed)
        self.event_manager.subscribe(self._on_model_dropped)
        self.event_manager.subscribe(self._on_diagram_selection_changed)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        if Gtk.get_major_version() == 3:
            scrolled_window.add(view)
        else:
            scrolled_window.set_child(view)
        scrolled_window.show()
        view.show()

        view.connect("row-activated", self._on_view_row_activated)
        view.connect_after("cursor-changed", self._on_view_cursor_changed)
        view.connect("destroy", self._on_view_destroyed)

        action_group, shortcuts = create_action_group(self, "tree-view")
        view.insert_action_group("tree-view", action_group)

        if Gtk.get_major_version() == 3:
            ctrl = Gtk.GestureMultiPress.new(view)
            ctrl.set_button(Gdk.BUTTON_SECONDARY)
            ctrl.connect("pressed", self._on_show_popup)
            self.ctrl.add(ctrl)

            ctrl = Gtk.EventControllerKey.new(view)
            ctrl.connect("key-pressed", self._on_edit_pressed)
            self.ctrl.add(ctrl)
        else:
            ctrl = Gtk.ShortcutController.new_for_model(shortcuts)
            ctrl.set_scope(Gtk.ShortcutScope.LOCAL)
            view.add_controller(ctrl)

            ctrl = Gtk.GestureClick.new()
            ctrl.set_button(Gdk.BUTTON_SECONDARY)
            ctrl.connect("pressed", self._on_show_popup)
            view.add_controller(ctrl)

        self.view = view
        self.scrolled_window = scrolled_window
        self.model.refresh()

        return scrolled_window

    def close(self):
        self.ctrl.clear()
        if self.view:
            if Gtk.get_major_version() == 3:
                self.view.destroy()
            elif self.scrolled_window:
                self.scrolled_window.unparent()
            self.view = None
            self.scrolled_window = None
        if self.model:
            self.model.shutdown()
            self.model = None
        self.event_manager.unsubscribe(self._on_model_refreshed)
        self.event_manager.unsubscribe(self._on_model_dropped)
        self.event_manager.unsubscribe(self._on_diagram_selection_changed)

    @event_handler(NamespaceModelRefreshed)
    def _on_model_refreshed(self, event):
        # Expand all root elements:
        if self.view:
            self.view.expand_row(path=Gtk.TreePath.new_first(), open_all=False)
            self._on_view_cursor_changed(self.view)

    @event_handler(NamespaceModelElementDropped)
    def _on_model_dropped(self, event):
        element = event.element
        self.select_element(element)

    @event_handler(DiagramSelectionChanged)
    def _on_diagram_selection_changed(self, event):
        focused_item = event.focused_item
        if isinstance(focused_item, Presentation) and focused_item.subject:
            self.select_element(focused_item.subject)

    def _on_show_popup(self, ctrl, n_press, x, y):
        if Gtk.get_major_version() == 3:
            menu = Gtk.Menu.new_from_model(popup_model(self.get_selected_element()))
            menu.attach_to_widget(self.view, None)
            menu.popup_at_pointer(None)
        else:
            menu = Gtk.PopoverMenu.new_from_model(
                popup_model(self.get_selected_element())
            )
            menu.set_pointing_to(Gdk.Rectangle(x, y, 1, 1))
            menu.set_offset(x, y)
            menu.set_has_arrow(False)
            menu.set_parent(self.view)
            menu.popup()

    def _on_edit_pressed(self, ctrl, keyval, keycode, state):
        if keyval == Gdk.KEY_F2:
            self.tree_view_rename_selected()
            return True
        return False

    def _on_view_row_activated(self, view, path, column):
        """Double click on an element in the tree view."""
        if Gtk.get_major_version() == 3:
            view.get_action_group("tree-view").lookup_action("open").activate()
        else:
            view.activate_action("tree-view.open", None)

    def _on_view_cursor_changed(self, view):
        """Another row is selected, toggle action sensitivity."""
        element = self.get_selected_element()
        if Gtk.get_major_version() == 3:
            action_group = view.get_action_group("tree-view")

            action_group.lookup_action("open").set_enabled(isinstance(element, Diagram))
            action_group.lookup_action("create-diagram").set_enabled(
                isinstance(element, UML.Package)
                or (element and isinstance(element.owner, UML.Package))
            )
            action_group.lookup_action("create-package").set_enabled(
                isinstance(element, UML.Package)
            )
            action_group.lookup_action("delete").set_enabled(
                isinstance(element, Diagram)
                or (isinstance(element, UML.Package) and not element.presentation)
            )
            action_group.lookup_action("rename").set_enabled(
                isinstance(element, UML.NamedElement)
            )
        else:
            # TODO: GTK4 - enable/disable actions based on view state
            pass

    def _on_view_destroyed(self, widget):
        self.close()

    def select_element(self, element: Element) -> None:
        """Select an element from the Namespace view.

        The element is selected. After this an action may be executed,
        such as OpenModelElement, which will try to open the element (if
        it's a Diagram).
        """
        assert self.model
        assert self.view

        model = self.view.get_model()
        tree_iter = self.model.iter_for_element(element)
        if not tree_iter:
            return

        path = model.get_path(tree_iter)
        path_indices = path.get_indices()

        # Expand the parent row
        if len(path_indices) > 1:
            parent_path = Gtk.TreePath.new_from_indices(path_indices[:-1])
            self.view.expand_row(path=parent_path, open_all=False)

        selection = self.view.get_selection()
        selection.select_path(path)
        self.view.scroll_to_cell(path, None, False, 0, 0)
        self._on_view_cursor_changed(self.view)

    def get_selected_element(self) -> Optional[Element]:
        assert self.view
        selection = self.view.get_selection()
        model, iter = selection.get_selected()
        if not iter:
            return None
        return model.get_value(iter, 0)  # type: ignore[no-any-return]

    @action(name="tree-view.open")
    def tree_view_open_selected(self):
        element = self.get_selected_element()
        if isinstance(element, Diagram):
            self.event_manager.handle(DiagramOpened(element))
        else:
            log.debug(f"No action defined for element {type(element).__name__}")

    @action(name="tree-view.show-in-diagram")
    def tree_view_show_in_diagram(self, diagram_id: str):
        element = self.element_factory.lookup(diagram_id)
        self.event_manager.handle(DiagramOpened(element))

    @action(name="tree-view.rename", shortcut="F2")
    def tree_view_rename_selected(self):
        assert self.view
        view = self.view
        element = self.get_selected_element()
        if element not in (None, RELATIONSHIPS):
            selection = view.get_selection()
            model, iter = selection.get_selected()
            path = model.get_path(iter)
            column = view.get_column(0)
            cell = column.get_cells()[1]
            cell.set_property("editable", 1)
            view.set_cursor(path, column, True)
            cell.set_property("editable", 0)

    @action(name="tree-view.create-diagram")
    @transactional
    def tree_view_create_diagram(self):
        assert self.view
        element = self.get_selected_element()
        assert element
        while not isinstance(element, UML.Package):
            element = element.owner
        diagram = self.element_factory.create(Diagram)
        diagram.package = element

        diagram.name = f"{element.name} diagram" if element else "New diagram"
        self.select_element(diagram)
        self.event_manager.handle(DiagramOpened(diagram))
        self.tree_view_rename_selected()

    @action(name="tree-view.create-package")
    @transactional
    def tree_view_create_package(self):
        element = self.get_selected_element()
        assert isinstance(element, UML.Package)
        package = self.element_factory.create(UML.Package)
        package.package = element

        package.name = f"{element.name} package" if element else "New model"
        self.select_element(package)
        self.tree_view_rename_selected()

    @action(name="tree-view.delete")
    @transactional
    def tree_view_delete(self):
        element = self.get_selected_element()
        if isinstance(element, UML.Package):
            element.unlink()
        elif isinstance(element, Diagram):
            m = Gtk.MessageDialog(
                None,
                Gtk.DialogFlags.MODAL,
                Gtk.MessageType.QUESTION,
                Gtk.ButtonsType.YES_NO,
                "Do you really want to delete diagram %s?\n\n"
                "This will possibly delete diagram items\n"
                "that are not shown in other diagrams." % (element.name or "<None>"),
            )
            if m.run() == Gtk.ResponseType.YES:
                for i in reversed(list(element.get_all_items())):
                    s = i.subject
                    if s and len(s.presentation) == 1:
                        s.unlink()
                    i.unlink()
                element.unlink()
            m.destroy()
