/* Runs theme/search.js against a stand-in DOM to check give_up: the
   request's timeout wiring, and where the focus goes when the field
   removes itself while it was focused. Used by tests/test_scripts.py,
   under node; no dependency. */
"use strict";
var fs = require("fs");
var vm = require("vm");

function Element(tag) {
	this.nodeName = tag.toUpperCase();
	this.attrs = {};
	this.children = [];
	this.parentNode = null;
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
Element.prototype.hasAttribute = function (k) {
	return Object.prototype.hasOwnProperty.call(this.attrs, k);
};
Element.prototype.appendChild = function (c) { this.children.push(c); c.parentNode = this; return c; };
Element.prototype.addEventListener = function (type, fn) { this.listeners[type] = fn; };
Element.prototype.focus = function () { document.activeElement = this; };
Object.defineProperty(Element.prototype, "innerHTML", {
	set: function () { this.children = []; }, get: function () { return ""; }
});

/* A tiny "a b" descendant selector, enough for ".collection-nav a". */
function matches(el, part) {
	if (part.charAt(0) === ".") {
		return (" " + el.className + " ").indexOf(" " + part.slice(1) + " ") !== -1;
	}
	return el.nodeName === part.toUpperCase();
}
function collect(el, part, out) {
	el.children.forEach(function (c) {
		if (matches(c, part)) {
			out.push(c);
		}
		collect(c, part, out);
	});
}
Element.prototype.querySelector = function (sel) {
	var scope = [this];
	sel.split(" ").forEach(function (part) {
		var next = [];
		scope.forEach(function (s) {
			var found = [];
			collect(s, part, found);
			next = next.concat(found);
		});
		scope = next;
	});
	return scope[0] || null;
};

var withNav = process.argv[3] === "nav";
var side = new Element("details");
side.className = "doc-side";
var box = new Element("div");
box.setAttribute("data-search-index", "docs/search-index.json");
side.appendChild(box);
if (withNav) {
	var nav = new Element("nav");
	nav.className = "collection-nav";
	nav.appendChild(new Element("a"));
	side.appendChild(nav);
}

var document = {
	activeElement: null,
	querySelector: function (sel) { return sel === "[data-search-index]" ? box : null; },
	createElement: function (tag) { return new Element(tag); }
};

var requested = [];
var lastReq = null;
function XMLHttpRequest() {}
XMLHttpRequest.prototype.open = function (method, url) { requested.push(url); };
XMLHttpRequest.prototype.send = function () { lastReq = this; };

var source = fs.readFileSync(process.argv[2], "utf8");
var context = { document: document, window: {}, XMLHttpRequest: XMLHttpRequest, String: String };
vm.runInNewContext(source, context);

var input = box.children[1];
input.listeners.focus();       /* triggers load(): opens and sends the request */
document.activeElement = input;

var mode = process.argv[4];
if (mode === "timeout") {
	lastReq.ontimeout();
} else if (mode === "abort") {
	lastReq.onabort();
} else {
	lastReq.onerror();
}

var focused = "other";
if (document.activeElement === input) {
	focused = "input";
} else if (document.activeElement === side) {
	focused = "side";
} else if (document.activeElement && document.activeElement.nodeName === "A") {
	focused = "link";
} else if (!document.activeElement) {
	focused = "none";
}

console.log(JSON.stringify({
	requested: requested,
	timeout: lastReq.timeout,
	has_ontimeout: typeof lastReq.ontimeout === "function",
	has_onabort: typeof lastReq.onabort === "function",
	hidden: box.hidden,
	focused: focused,
	side_tabindex: side.getAttribute("tabindex")
}));
