class VoiceRecorder {
	constructor() {
		this.recClicked = false;
		this.media = null;
		this.recBlob = null;
		this.recForm = null;
	}
	recordOnclick(btn, onstop=()=>{}) {
		btn = helpTools.bs(btn);
		let that = this;

		btn.addEventListener('click', function () {
			if (!that.recClicked) {
				that.startRec();
				that.recClicked = true;
			} else {
				that.media.stop();
				that.recClicked = false;
				that.media.addEventListener("dataavailable",function(event) {
					that.recBlob = new Blob([event.data], {type: 'audio/wav'});
					let fd = new FormData;
					fd.append('file', that.recBlob);
					that.recForm = fd;
					onstop(that.recBlob);
				});
			}
		});
	}
	startRec() {
		this.recBlob = null;
		this.recForm = null;
		navigator.mediaDevices.getUserMedia({audio: true}).then(stream => {
			this.media = new MediaRecorder(stream);
			this.media.start();
		});
	}
	stopRec() {
		let that = this;
		this.media.stop();
		this.media.addEventListener("dataavailable",function(event) {
			that.recBlob = new Blob([event.data], {type: 'audio/wav'});
			let fd = new FormData;
			fd.append('file', that.recBlob);
			that.recForm = fd
		});
	}
}

var helpTools = {
	bs: (id) => document.querySelector(id),
	bn: (id) => document.getElementsByName(id),
	bi: (id) => document.getElementById(id),
	rd: (id) => {
		helpTools.beta.changeStyle(`#${id}`, {filter: 'brightness(1)', transition: 'filter 0.2s linear'});
		helpTools.beta.changeStyle(`#${id}:hover`, {filter: 'brightness(0.8)'});
	},

	htmlEscape(text, allowed=[]) {
		text = text.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
		
		for (i of allowed) {
			let escaped = i.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;').replaceAll("'", '&#39;');
			text = text.replaceAll(escaped, i);
		}
		return text;
	},

	htmlUnescape(text) {
			text = text.replaceAll('&amp;', '&').replaceAll('&lt;', '<').replaceAll('&gt;', '>').replaceAll('&quot;', '"').replaceAll("&#39;", "'");
			return text;
		},

	prepChild(parent, child, p='afterbegin') {
		helpTools.bs(parent).insertAdjacentHTML(p, child);
	},

	getCookie(name) {
  		let cookie = document.cookie.match(new RegExp("(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"));
 		return cookie ? decodeURIComponent(cookie[1]) : undefined;
	},

	syncGet(url) {
		let xhr = new XMLHttpRequest();
		xhr.open('GET', url, false);
		xhr.send();
		return xhr.response;
	},

	anim(elem, onstop="nothing") {
		if (helpTools.bi('hlptls-style-anim') === null) {
			helpTools.prepChild('head', `<style id="hlptls-style-anim">@keyframes hlptls-flip {0%{transform:perspective(500px)rotateX(0deg)}100%{transform:perspective(500px)rotateX(-90deg)}}.hlptls-flip{animation:hlptls-flip 300ms ease;transform-origin: 50% 0%}.hlptls-fade{transition:opacity 12s linear}</style>`, 'beforeend');
		} else {
			helpTools.bi('hlptls-style-anim').textContent = `@keyframes hlptls-flip {0%{transform:perspective(500px)rotateX(0deg)}100%{transform:perspective(500px)rotateX(-90deg)}}.hlptls-flip{animation:hlptls-flip 300ms ease;transform-origin: 50% 0%}.hlptls-fade{transition:opacity 12s linear}`;
		}
		if (typeof elem !== 'object') elem=helpTools.bs(elem);
		try{onstop = onstop.toLowerCase()}catch{}
		if (onstop === 'delelem' || onstop === 'delete') {onstop = () => {elem.remove()}
		} else if (onstop === 'hide') {onstop = () => {elem.style.visibility = 'hidden';}
		} else if (onstop === "nothing") {onstop = () => {}}

		animList = {
			fade(direction='in', duration=0.5) {
				helpTools.bi('hlptls-style-anim').textContent = helpTools.bi('hlptls-style-anim').textContent.replaceAll('12s', `${duration}s`)

				if (direction === 'out') {
					elem.style.visibility = '';
					elem.style.opacity = '0';
					elem.classList.add('hlptls-fade');
					elem.style.opacity = '1';
				}
				else if (direction === 'in') {
					elem.style.opacity = '1';
					elem.classList.add('hlptls-fade');
					elem.style.opacity = '0';
				}
				setTimeout(onstop, duration * 1000)
			},
			flip(duration=0.5) {
				helpTools.bi('hlptls-style-anim').textContent = helpTools.bi('hlptls-style-anim').textContent.replaceAll('300ms', `${duration}s`);
				elem.classList.add('hlptls-flip');
				setTimeout(() => {
					onstop();
					elem.classList.remove('hlptls-flip');
				}, duration * 1000)
			}
		}
		return animList;
	},

	timer: class {
		constructor(id) {
			this.elem = helpTools.bs(id);
			this.elem.textContent = '0:00';
			this.min = 0;
			this.sec = 0;
			try {
				helpTools.data.timers.push(this)
			}catch{helpTools.data.timers=[this]}
		}
		start() {
			let that = this;
			this.interval = setInterval(function(){
				that.sec++
				if (that.sec === 60) {
					that.sec = 0;
					that.min++;
				}
				let local_sec = `${that.sec}`;
				if (that.sec <= 9) {
					local_sec = `0${that.sec}`;
				}
				that.elem.textContent = `${that.min}:${local_sec}`
			}, 1000)
		}
		pause() {
			clearInterval(this.interval)
			this.interval = null;
			return this.elem.textContent;
		}
		drop() {
			try{clearInterval(this.interval)}catch{}
			const time = this.elem.textContent;
			this.interval = null;
			this.sec = 0;
			this.min = 0;
			this.elem.textContent = `0:00`;
			return time;
		}
	},

	beta: {
		changeStyle(selector, newRule) {
			let s = helpTools.bi('hlptls-user-style');
			if (s === null) {
				helpTools.prepChild('head', '<style id="hlptls-user-style"></style>', 'beforeend');
				s = helpTools.bi('hlptls-user-style');
			}
			s.textContent = s.textContent.replaceAll(selector, '.hlptls-useless')

			values = '';
			for (i in newRule) {
				let v = newRule[i].replaceAll('!important', '').replaceAll(';', '');
				values += `${i}: ${v}!important;`;
			}

			s.append(`\n${selector} {${values}}`)
		},
	},
	data: {}
}
