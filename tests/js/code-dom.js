/* Runs theme/code.js against a stand-in DOM: one pre.code block, no
   clipboard API (forces the execCommand fallback), and checks that a
   click on the copy button restores focus to it once the temporary
   textarea is gone. Used by tests/test_scripts.py, under node; no
   dependency. */
"use strict";
var fs = require("fs");
var vm = require("vm");

function Element(tag) {
	this.nodeName = tag.toUpperCase();
	this.attrs = {};
	this.children = [];
	this.parentNode = null;
	this.textContent = "";
	this.className = "";
	this.listeners = {};
}
Element.prototype.getAttribute = function (k) {
	return Object.prototype.hasOwnProperty.call(this.attrs, k) ? this.attrs[k] : null;
};
Element.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
Element.prototype.appendChild = function (c) {
	if (c.parentNode) {
		var was = c.parentNode.children.indexOf(c);
		if (was !== -1) {
			c.parentNode.children.splice(was, 1);
		}
	}
	this.children.push(c);
	c.parentNode = this;
	return c;
};
Element.prototype.removeChild = function (c) {
	var i = this.children.indexOf(c);
	if (i !== -1) {
		this.children.splice(i, 1);
	}
	c.parentNode = null;
	return c;
};
Element.prototype.insertBefore = function (node, ref) {
	var i = this.children.indexOf(ref);
	this.children.splice(i === -1 ? this.children.length : i, 0, node);
	node.parentNode = this;
	return node;
};
Element.prototype.addEventListener = function (type, fn) { this.listeners[type] = fn; };
Element.prototype.select = function () {};
Element.prototype.focus = function () { document.activeElement = this; };
Element.prototype.querySelector = function (sel) {
	for (var i = 0; i < this.children.length; i++) {
		if (this.children[i].nodeName === sel.toUpperCase()) {
			return this.children[i];
		}
	}
	return null;
};

var wrapper = new Element("div");
var pre = new Element("pre");
pre.className = "code";
var code = new Element("code");
code.textContent = "example";
pre.appendChild(code);
wrapper.appendChild(pre);

var me = new Element("script");
me.setAttribute("data-copy", "copy");
me.setAttribute("data-copied", "copied");

var body = new Element("body");
var document = {
	activeElement: null,
	currentScript: me,
	body: body,
	createElement: function (tag) { return new Element(tag); },
	querySelectorAll: function () { return [pre]; },
	execCommand: function () { return true; }
};

var navigator = {};   /* no clipboard: forces the execCommand fallback */
var window = { isSecureContext: false };

var source = fs.readFileSync(process.argv[2], "utf8");
var context = {
	document: document, navigator: navigator, window: window,
	setTimeout: function () { return 0; }, clearTimeout: function () {}
};
vm.runInNewContext(source, context);

var box = wrapper.children[0];
var button = box.children[1];
button.listeners.click();

console.log(JSON.stringify({
	button_text: button.textContent,
	body_children: body.children.length,
	focused_button: document.activeElement === button
}));
