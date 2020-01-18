"use strict";
var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (b.hasOwnProperty(p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
Object.defineProperty(exports, "__esModule", { value: true });
var React = require("react");
var BubbleGroup_1 = require("../BubbleGroup");
var ChatBubble_1 = require("../ChatBubble");
var ChatInput_1 = require("../ChatInput");
var styles_1 = require("./styles");
var ChatFeed = (function (_super) {
    __extends(ChatFeed, _super);
    function ChatFeed(props) {
        return _super.call(this, props) || this;
    }
    ChatFeed.prototype.componentDidMount = function () {
        this.scrollToBottom();
    };
    ChatFeed.prototype.componentDidUpdate = function () {
        this.scrollToBottom();
    };
    ChatFeed.prototype.scrollToBottom = function () {
        var scrollHeight = this.chat.scrollHeight;
        var height = this.chat.clientHeight;
        var maxScrollTop = scrollHeight - height;
        this.chat.scrollTop = maxScrollTop > 0 ? maxScrollTop : 0;
    };
    ChatFeed.prototype.renderMessages = function (messages) {
        var _a = this.props, isTyping = _a.isTyping, bubbleStyles = _a.bubbleStyles, chatBubble = _a.chatBubble, showSenderName = _a.showSenderName;
        var ChatBubble = chatBubble || ChatBubble_1.default;
        var group = [];
        var messageNodes = messages.map(function (message, index) {
            group.push(message);
            if (index === messages.length - 1 || messages[index + 1].id !== message.id) {
                var messageGroup = group;
                group = [];
                return (React.createElement(BubbleGroup_1.default, { key: index, messages: messageGroup, id: parseInt(message.id.toString(), 10), showSenderName: showSenderName, chatBubble: ChatBubble, bubbleStyles: bubbleStyles }));
            }
            return null;
        });
        if (this.props.empty) {
            messageNodes.unshift(React.createElement("div", { key: 'ldextra', style: __assign({}, styles_1.default.chatbubbleWrapper) }, this.props.extraMsg));
        }
        if (isTyping) {
            messageNodes.push(React.createElement("div", { key: "isTyping", style: __assign({}, styles_1.default.chatbubbleWrapper) }, this.props.typingMsg));
        }
        if (this.props.showEnd) {
            messageNodes.push(React.createElement("div", { key: "showEnd", style: __assign({}, styles_1.default.chatbubbleWrapper) }, this.props.showEndMsg));
        }
        return messageNodes;
    };
    ChatFeed.prototype.render = function () {
        var _this = this;
        var inputField = this.props.hasInputField && React.createElement(ChatInput_1.default, null);
        var maxHeight = this.props.maxHeight;
        return (React.createElement("div", { id: "chat-panel", style: styles_1.default.chatPanel },
            React.createElement("div", { ref: function (c) {
                    _this.chat = c;
                }, className: "chat-history", style: __assign(__assign({}, styles_1.default.chatHistory), { maxHeight: maxHeight }) },
                React.createElement("div", { className: "chat-messages" }, this.renderMessages(this.props.messages))),
            inputField));
    };
    return ChatFeed;
}(React.Component));
exports.default = ChatFeed;
//# sourceMappingURL=index.js.map