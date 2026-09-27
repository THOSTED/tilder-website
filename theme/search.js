/* Documentation search. The doc layout's left column holds an empty
   <div data-search-index>: this script fills it with a labelled search
   field and a list of results, and reads the collection's index (written
   by the doc type, one per language) on first focus. Every word comes
   from the div's data-* attributes; without JavaScript nothing is shown.
   ES5, same-origin, no storage. */
(function () {
	"use strict";

	var MAX = 10;
	var WEIGHTS = [["t", 8], ["h", 4], ["d", 2], ["x", 1]];

	/* Lower case, accents removed: "Élan" and "elan" match. */
	function fold(s) {
		s = String(s).toLowerCase();
		if (s.normalize) {
			s = s.normalize("NFD").replace(/[̀-ͯ]/g, "");
		}
		return s;
	}

	/* Each record's fields folded once: title, headings, description, text. */
	function prepare(index) {
		var out = [], i;
		for (i = 0; i < index.length; i++) {
			out.push({
				item: index[i],
				t: fold(index[i].t || ""),
				h: fold((index[i].h || []).join(" ")),
				d: fold(index[i].d || ""),
				x: fold(index[i].x || "")
			});
		}
		return out;
	}

	/* The records every word of the query appears in, best first: a word
	   in the title outweighs one in a heading, then the description, then
	   the text. Ties keep the index's order, the collection's. */
	function search(prepared, query) {
		var words = fold(query).split(/\s+/), hits = [], i, j, k, score, best;
		words = words.filter(function (w) { return w !== ""; });
		if (!words.length) {
			return [];
		}
		for (i = 0; i < prepared.length; i++) {
			score = 0;
			for (j = 0; j < words.length; j++) {
				best = 0;
				for (k = 0; k < WEIGHTS.length; k++) {
					if (prepared[i][WEIGHTS[k][0]].indexOf(words[j]) !== -1) {
						best = WEIGHTS[k][1];
						break;
					}
				}
				if (!best) {
					score = 0;
					break;
				}
				score += best;
			}
			if (score) {
				hits.push({ item: prepared[i].item, score: score, order: i });
			}
		}
		hits.sort(function (a, b) { return b.score - a.score || a.order - b.order; });
		return hits.map(function (h) { return h.item; });
	}

	if (typeof module === "object" && module.exports) {   /* the tests, under node */
		module.exports = { fold: fold, prepare: prepare, search: search, MAX: MAX };
		return;
	}

	var box = document.querySelector("[data-search-index]");
	/* No index on this page, or already done (the script is linked by the
	   layout and, on a page that lists docs, by the type too). */
	if (!box || !box.getAttribute("data-search-index") || box.getAttribute("data-search-ready")) {
		return;
	}
	box.setAttribute("data-search-ready", "true");

	var home = box.getAttribute("data-home") || "";
	var url = home + box.getAttribute("data-search-index");
	var countText = box.getAttribute("data-count") || "{n}";
	var noneText = box.getAttribute("data-none") || "";
	var prepared = null, loading = false, selected = -1, links = [];

	function make(tag, cls) {
		var el = document.createElement(tag);
		if (cls) {
			el.className = cls;
		}
		return el;
	}

	var label = make("label", "doc-search-label");
	var input = make("input", "doc-search-input");
	var status = make("p", "doc-search-status");
	var list = make("ul", "doc-search-results");
	label.htmlFor = "doc-search-input";
	label.textContent = box.getAttribute("data-label") || "";
	input.type = "search";
	input.id = "doc-search-input";
	input.placeholder = box.getAttribute("data-placeholder") || "";
	input.autocomplete = "off";
	input.spellcheck = false;
	input.setAttribute("role", "combobox");
	input.setAttribute("aria-autocomplete", "list");
	input.setAttribute("aria-expanded", "false");
	input.setAttribute("aria-controls", "doc-search-results");
	status.setAttribute("aria-live", "polite");
	list.id = "doc-search-results";
	list.setAttribute("role", "listbox");
	list.hidden = true;
	box.appendChild(label);
	box.appendChild(input);
	box.appendChild(status);
	box.appendChild(list);

	/* The index cannot be read (offline, blocked): the field goes away. */
	function give_up() {
		box.innerHTML = "";
		box.hidden = true;
	}

	function load() {
		if (prepared || loading) {
			return;
		}
		loading = true;
		var req = new XMLHttpRequest();
		req.open("GET", url);
		req.onload = function () {
			try {
				if (req.status !== 200) {
					throw new Error(String(req.status));
				}
				prepared = prepare(JSON.parse(req.responseText));
			} catch (e) {
				give_up();
				return;
			}
			run();
		};
		req.onerror = give_up;
		req.send();
	}

	function choose(i) {
		var items = list.children, k;
		selected = i;
		for (k = 0; k < items.length; k++) {
			items[k].setAttribute("aria-selected", k === i ? "true" : "false");
		}
		if (i >= 0) {
			input.setAttribute("aria-activedescendant", items[i].id);
		} else {
			input.removeAttribute("aria-activedescendant");
		}
	}

	function run() {
		var query = input.value, hits, i, li, a, span;
		list.innerHTML = "";
		links = [];
		selected = -1;
		input.removeAttribute("aria-activedescendant");
		if (!prepared || !query.replace(/\s+/g, "")) {
			list.hidden = true;
			input.setAttribute("aria-expanded", "false");
			status.textContent = "";
			return;
		}
		hits = search(prepared, query);
		for (i = 0; i < hits.length && i < MAX; i++) {
			li = make("li");
			li.id = "doc-search-result-" + i;
			li.setAttribute("role", "option");
			li.setAttribute("aria-selected", "false");
			a = make("a");
			a.href = home + hits[i].u;
			a.textContent = hits[i].t;
			if (hits[i].d) {
				span = make("span");
				span.textContent = hits[i].d;
				a.appendChild(span);
			}
			li.appendChild(a);
			list.appendChild(li);
			links.push(a);
		}
		list.hidden = !links.length;
		input.setAttribute("aria-expanded", links.length ? "true" : "false");
		status.textContent = hits.length ? countText.replace("{n}", String(hits.length)) : noneText;
	}

	input.addEventListener("focus", load);
	input.addEventListener("input", run);
	input.addEventListener("keydown", function (e) {
		var key = e.key || "";
		if ((key === "ArrowDown" || e.keyCode === 40) && links.length) {
			choose(selected + 1 < links.length ? selected + 1 : 0);
			e.preventDefault();
		} else if ((key === "ArrowUp" || e.keyCode === 38) && links.length) {
			choose(selected > 0 ? selected - 1 : links.length - 1);
			e.preventDefault();
		} else if ((key === "Enter" || e.keyCode === 13) && selected >= 0) {
			window.location.href = links[selected].href;
			e.preventDefault();
		} else if (key === "Escape" || key === "Esc" || e.keyCode === 27) {
			input.value = "";
			run();
		}
	});
})();
