# -*- coding: utf-8 -*-
import deltachat as dc
import urwid
import urwid_readline

from ..event import ChatListMonitor


def get_subtitle(chat):
    members = chat.get_contacts()
    if not chat.is_group() and members:
        return members[0].addr
    else:
        return "{} member(s)".format(len(members))


class MessageSendWidget(urwid.Filler, ChatListMonitor):
    def __init__(self, keymap, account):
        self.text_caption = " >> "
        self.status_bar = urwid.Text(("status_bar", " "), align="left")
        self.attr = urwid.AttrMap(self.status_bar, "status_bar")

        self.widgetEdit = urwid_readline.ReadlineEdit(
            self.text_caption, "", multiline=True
        )

        self.pile = urwid.Pile([self.attr, self.widgetEdit])
        super().__init__(self.pile)

        self.model = account
        self.keymap = keymap
        self.current_chat = None
        self.typing = False

        self.model.add_chatlist_monitor(self)

    def chatlist_changed(self, current_chat_index, chats):
        if self.current_chat is None:
            self.chat_selected(current_chat_index, chats)
        else:
            self.update_status_bar(current_chat_index, chats)

    def chat_selected(self, index, chats):
        if index is not None and self.current_chat == chats[index]:
            return
        self.typing = False
        # save draft
        if self.current_chat:
            text = self.widgetEdit.get_edit_text()
            prev_draft = self.current_chat.get_draft()
            if not prev_draft or prev_draft.text != text:
                msg = dc.Message.new_empty(self.current_chat.account, "text")
                msg.set_text(text)
                self.current_chat.set_draft(msg)
        if index is None:
            self.current_chat = None
            return
        self.current_chat = chats[index]
        # load draft
        msg = self.current_chat.get_draft()
        self.widgetEdit.set_edit_text(msg.text if msg else "")
        # update status bar
        self.update_status_bar(index, chats)

    def update_status_bar(self, current_chat_index, chats):
        if current_chat_index is None:
            text = ""
        else:
            chat = chats[current_chat_index]
            verified = ""
            if chat.is_protected():
                verified = "✓ "
            text = " {}[ {} ] -- {}".format(
                verified, chat.get_name(), get_subtitle(chat)
            )

        self.status_bar.set_text(text)

    def keypress(self, size, key):
        key = super().keypress(size, key)
        # save draft on exit
        if key == self.keymap["quit"]:
            if not self.current_chat:
                return
            text = self.widgetEdit.get_edit_text()
            prev_draft = self.current_chat.get_draft()
            if not prev_draft or prev_draft.text != text:
                msg = dc.Message.new_empty(self.current_chat.account, "text")
                msg.set_text(text)
                self.current_chat.set_draft(msg)
        # save draft on first type
        elif not key and not self.typing and self.current_chat:
            text = self.widgetEdit.get_edit_text()
            draft = self.current_chat.get_draft()
            if not draft or draft.text != text:
                self.typing = True
                msg = dc.Message.new_empty(self.current_chat.account, "text")
                msg.set_text(text)
                self.current_chat.set_draft(msg)

        return key
