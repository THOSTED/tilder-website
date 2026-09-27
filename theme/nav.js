/* The doc layout on screens of every width. The sidebar (<details
   data-doc-side>) is open in the markup, so it works without JavaScript:
   on a small screen this script folds it, and folds it again once a link
   in it is followed. On a wide screen it moves the page's [TOC] into the
   right column (data-doc-toc) and opens it; narrower, it puts it back.
   ES5, no text of its own, no storage. */
(function () {
	"use strict";

	if (!window.matchMedia) {
		return;
	}
	var narrow = window.matchMedia("(max-width: 45rem)");
	var wide = window.matchMedia("(min-width: 60rem)");

	function watch(query, fn) {
		if (query.addEventListener) {
			query.addEventListener("change", fn);
		} else if (query.addListener) {
			query.addListener(fn);
		}
	}

	/* The sidebar: folded on small screens, always open on the others. */
	var side = document.querySelector("[data-doc-side]");
	if (side) {
		var fit = function () {
			side.open = !narrow.matches;
		};
		fit();
		watch(narrow, fit);
		side.addEventListener("click", function (e) {
			var t = e.target;
			while (t && t !== side && t.nodeName !== "A") {
				t = t.parentNode;
			}
			if (t && t.nodeName === "A" && narrow.matches) {
				side.open = false;
			}
		});
	}

	/* The [TOC]: in the right column on wide screens, in the text else. */
	var slot = document.querySelector("[data-doc-toc]");
	var toc = document.querySelector("main .toc");
	if (slot && toc) {
		var home = document.createComment("toc");
		var box = slot.parentNode;
		var details = toc.querySelector("details");
		toc.parentNode.insertBefore(home, toc);
		var place = function () {
			if (wide.matches) {
				slot.appendChild(toc);
				slot.hidden = false;
				if (details) {
					details.open = true;
				}
				box.className += /\bdoc--toc\b/.test(box.className) ? "" : " doc--toc";
			} else {
				home.parentNode.insertBefore(toc, home.nextSibling);
				slot.hidden = true;
				if (details) {
					details.open = false;
				}
				box.className = box.className.replace(/\s*\bdoc--toc\b/, "");
			}
		};
		place();
		watch(wide, place);
	}
})();
