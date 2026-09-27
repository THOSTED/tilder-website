/* A copy button on every code block (tilder's code.js: loaded only on
   pages with code). Its words come from its own <script> tag, data-copy
   and data-copied (labels.copy, labels.copied in site.toml). It copies the
   code as plain text, without the highlighting. ES5, no storage. */
(function () {
	"use strict";

	var me = document.currentScript || document.querySelector("script[data-copy]");
	if (!me) {
		return;
	}
	var copy = me.getAttribute("data-copy") || "";
	var copied = me.getAttribute("data-copied") || copy;

	function fallback(text, done, button) {
		var area = document.createElement("textarea");
		area.value = text;
		area.setAttribute("readonly", "");
		area.className = "sr-only";
		document.body.appendChild(area);
		area.select();
		try {
			if (document.execCommand("copy")) {
				done();
			}
		} catch (e) {
			/* nothing copied: the reader selects the code by hand */
		}
		document.body.removeChild(area);
		/* The textarea held the focus (area.select()): give it back to
		   the button rather than leaving it on the removed element. */
		if (button && button.focus) {
			button.focus();
		}
	}

	function write(text, done, button) {
		if (navigator.clipboard && window.isSecureContext) {
			navigator.clipboard.writeText(text).then(done, function () {
				fallback(text, done, button);
			});
		} else {
			fallback(text, done, button);
		}
	}

	function add(pre) {
		var box = document.createElement("div");
		var button = document.createElement("button");
		var timer = null;
		box.className = "code-box";
		button.type = "button";
		button.className = "code-copy";
		button.textContent = copy;
		button.setAttribute("aria-live", "polite");
		pre.parentNode.insertBefore(box, pre);
		box.appendChild(pre);
		box.appendChild(button);
		button.addEventListener("click", function () {
			var code = pre.querySelector("code") || pre;
			write(code.textContent, function () {
				button.textContent = copied;
				clearTimeout(timer);
				timer = setTimeout(function () {
					button.textContent = copy;
				}, 2000);
			}, button);
		});
	}

	if (!copy) {
		return;
	}
	var blocks = document.querySelectorAll("pre.code");
	for (var i = 0; i < blocks.length; i++) {
		add(blocks[i]);
	}
})();
