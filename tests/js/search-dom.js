/* Runs theme/search.js twice against a tiny stand-in for the DOM, as the
   doc layout and a {docs} list both link it, and prints what it built as
   JSON. Used by tests/test_scripts.py, under node; no dependency. */
"use strict";
var fs = require("fs");
var vm = require("vm");

function Element(tag) {
	this.nodeName = tag.toUpperCase();
	this.attrs = {};
	this.children = [];
	this.hidden = false;
	this.textContent = "";
	this.value = "";
	this.className = "";
	this.listeners = {};
}
Element.prototype.getAttribute = function (k) {
	return Object.prototype.hasOwnProperty.call(this.attrs, k) ? this.attrs[k] : null;
};
Element.prototype.setAttribute = function (k, v) { this.attrs[k] = String(v); };
Element.prototype.removeAttribute = function (k) { delete this.attrs[k]; };
Element.prototype.appendChild = function (c) { this.children.push(c); return c; };
Element.prototype.addEventListener = function (type, fn) { this.listeners[type] = fn; };
Object.defineProperty(Element.prototype, "innerHTML", {
	set: function () { this.children = []; }, get: function () { return ""; }
});

var box = new Element("div");
var words = JSON.parse(process.argv[3]);
Object.keys(words).forEach(function (k) { box.setAttribute(k, words[k]); });
var document = {
	querySelector: function (sel) { return sel === "[data-search-index]" ? box : null; },
	createElement: function (tag) { return new Element(tag); }
};
var source = fs.readFileSync(process.argv[2], "utf8");
var requested = [];
function XMLHttpRequest() {}
XMLHttpRequest.prototype.open = function (method, url) { requested.push(url); };
XMLHttpRequest.prototype.send = function () {
	this.status = 200;
	this.responseText = process.argv[4] || "[]";
	this.onload();
};
var context = { document: document, window: {}, XMLHttpRequest: XMLHttpRequest, String: String };
vm.runInNewContext(source, context);
vm.runInNewContext(source, context);
var input = box.children[1], list = box.children[3], status = box.children[2];
if (input && process.argv[5] !== undefined) {
	input.listeners.focus();
	input.value = process.argv[5];
	input.listeners.input();
}
console.log(JSON.stringify({
	requested: requested,
	status: status ? status.textContent : null,
	results: list ? list.children.map(function (li) { return li.children[0].href; }) : [],
	ready: box.getAttribute("data-search-ready"),
	children: box.children.map(function (c) {
		return { tag: c.nodeName, cls: c.className, text: c.textContent,
			placeholder: c.placeholder || null, id: c.id || null };
	})
}));
