
I$(236, function (u, m, e, i, f, h, c, t, o, n, l, r, d, p, a, _, s, g, v, y, b) {
    s._$$IndexModule = u._$klass();
    pro = s._$$IndexModule._$extend(h);
    pro.__init = function (i) {
        this.__supInit(i);
        this.__getNodes();
        this.__addEvent();
        if (t(".m-imgslider-wrap .imgpagebox").length) c._$allocate({
                box: t(".m-imgslider-wrap .m-slide")[0],
                loop: !0,
                auto: !0,
                scrollTime: 200,
                callback: this._$sliderChange()
            });
        this.__initGlobalTemai();
        f._$$LazyImage._$allocate({
            attr: "src",
            oncheck: function (t) {
                var e = t.target.getAttribute("data-src");
                if (e) {
                    var i = t.target.getAttribute("src");
                    if (!i || i !== e);
                    else t.value = 0
                } else t.value = 0
            },
            onremove: function (t) {
                t.stopped = !0
            }
        });
        var n = navigator.userAgent,
            s = !! n.match(/(iPhone|iPod|iPad)/i);
        this.__globalpickTpl = r._$add(l);
        var e = "kaola://" + location.host + location.pathname;
        if (s) e = "kaola://";
        _._$open({
            openUrl: e,
            action: "open"
        })
    };
    pro.__getNodes = function () {
        this.__globalPick = document.querySelector(".m-globalpick");
        this.__go2Web = i._$get("toweb")
    };
    pro.__addEvent = function () {

    };

    pro.__triggerScrollEvt = function () {
        return n.debounce(function () {
            e._$dispatchEvent(window, "scroll")
        }, 200, !1)
    }();
    pro.__classReg = function (t) {
        return new RegExp("(\\s|^)" + t + "(\\s|$)")
    };
    pro.__findParent = function (e, i) {
        for (var t = e; t && "body" != t.tagName.toLowerCase();) {
            if (i.test(t.className)) return t;
            t = t.parentNode
        }
        return null
    };
    pro.__heightProcess = function (i) {
        var n = this.__classReg("imglist"),
            e = this.__findParent(i.target, n);
        if (e && "3" === e.getAttribute("data-type")) {
            e._banImgLoadCount = (e._banImgLoadCount || 0) + 1;
            if (3 !== e._banImgLoadCount) return;
            var t = e.querySelectorAll("img");
            if (3 === t.length && t[0].height !== t[1].height + t[2].height) t[0].height = t[1].height + t[2].height
        }
    };
    pro.__bannerlazyImgProcess = function (i) {
        var n = this.__classReg("imglist"),
            e = this.__classReg("s\\-lazy\\-loading"),
            t = this.__findParent(i.target, n);
        if (t && e.test(t.className)) t.className = t.className.replace(e, " ");
        this.__triggerScrollEvt()
    };
    pro._$sliderChange = function () {
        var e = t(".m-imgslider-wrap .imgpagebox");
        return function (t) {
            e._$children(".active", !0)._$delClassName("active");
            e._$children(".dot", !0)._$get(t, !0)._$addClassName("active")
        }
    };
    pro.__lazyImgLoad = function (t) {
        var e = this.__classReg("loading");
        if (e.test(t.target.className)) t.target.className = t.target.className.replace(e, " ");
        this.__triggerScrollEvt()
    };
    pro.__initGlobalTemai = function () {
        var e = this.__globalTemai = {}, i = t(".m-img-temai .timer-wrap"),
            n = i._$attr("data-servertime");
        e._openTime = +new Date;
        e._remainTime = parseFloat(i._$attr("data-timeleft")) || 0;
        e._needTimer = !0;
        try {
            if (sessionStorage.getItem("globalTemaiTimer") === n) e._openTime = parseFloat(sessionStorage.getItem(
                    "globalTemaiPageLoad")) || e._openTime;
            else {
                sessionStorage.setItem("globalTemaiTimer", n);
                sessionStorage.setItem("globalTemaiPageLoad", e._openTime)
            }
        } catch (o) {}
        this.__setRemainText(e._remainTime);
        if (!(e._remainTime <= 0)) var s = setInterval(function () {
                var t = this.__globalTemai._remainTime - (+new Date - this.__globalTemai._openTime);
                if (0 >= t) {
                    t = 0;
                    clearInterval(s);
                    this.__refreshTemai()
                } else this.__setRemainText(t)
            }._$bind(this), 1e3);
        else e._needTimer = !1
    };
    pro.__setRemainText = function (h) {

    };
    pro.__refreshTemai = function () {
        this.__getNewTemai(function (r, e) {
            if (!r && e.globalTemai && e.globalTemai.slidGoodsList && e.globalTemai.slidGoodsList.length > 0) {
                for (var i, o = "", s = 0; s < e.globalTemai.slidGoodsList.length; s++) {
                    i = e.globalTemai.slidGoodsList[s];
                    o += '<a href="/product/' + i.goodsId + '.html"><img src="' + n.imgThumbnailUrl(i.imageUrl, 600) +
                        '"></a>'
                }
                t(".m-img-temai .imgs")._$html(o);
                t(".m-img-temai .timer-wrap")._$attr("data-timeleft", e.globalTemai.endTimestamp - e.serverTime);
                this.__initGlobalTemai()
            } else t(".m-img-temai")._$style("display", "none")
        }._$bind(this))
    };
    pro.__getNewTemai = function (t) {
        o("/home/globaltemai.html", {
            method: "GET",
            norest: !0,
            type: "json",
            onload: function (e) {
                if (e && 1 == e.code && e.body) t && t(null, e.body);
                else t && t(1, e)
            },
            onerror: function (e) {
                t && t(1, e)
            }
        })
    };
    pro.__globalPickScrollCheck = function () {
        if ("undefined" == typeof this.__globalPick.__hasMore) {
            this.__globalPick.__hasMore = !! this.__globalPick.getAttribute("data-hasmore");
            this.__globalPick.__current = 1
        }
        var i = this.__globalPick.getBoundingClientRect(),
            e = i.top + i.height - window.innerHeight;
        if ("undefined" != typeof this.__globalPick.__lastOffsetTop) if (this.__globalPick.__lastOffsetTop >= e) this.__globalPick
                    .__orient = "flipdown";
            else this.__globalPick.__orient = "flipup";
        this.__globalPick.__lastOffsetTop = e;
        if (240 >= e && !this.__globalPick.__loading && this.__globalPick.__hasMore && "flipdown" === this.__globalPick
            .__orient) {
            t(".m-globalpick .m-loading")._$style("display", "block");
            this.__getGlobalPickList()
        }
    };
    pro.__getGlobalPickList = function () {
        var e = 10,
            i = "网络异常";
        this.__globalPick.__loading = !0;
        var n = {
            query: {
                offset: this.__globalPick.__current * e,
                limit: e
            },
            norest: !0,
            type: "json",
            method: "get",
            onload: function (e) {
                if (e && 1 === e.code && e.body) {
                    var n = e.body,
                        s = n.globalPick.data;
                    this.__globalPick.__current += 1;
                    this.__globalPick.__loading = !1;
                    this.__globalPick.__hasMore = n.hasMore;
                    if (s.length) {
                        var o = r._$get(this.__globalpickTpl, {
                            list: s
                        });
                        this.__globalPick.querySelector(".onsale-wrap").appendChild(t(o)[0])
                    }
                    if (!n.hasMore) {
                        this.__globalPick.querySelector(".nomore-data").style.display = "block";
                        t(".m-docfoot")._$style("display", "block")
                    }
                    this.__fireScrollEvt()
                } else {
                    t(".m-docfoot")._$style("display", "block");
                    a.show({
                        type: "error",
                        message: i,
                        duration: 2e3,
                        singleMsg: !0
                    });
                    setTimeout(function () {
                        window.scrollBy(0, -1);
                        this.__globalPick.__loading = !1
                    }._$bind(this), 2500)
                }
                t(".m-globalpick .m-loading")._$style("display", "none")
            }._$bind(this),
            onerror: function (e) {
                t(".m-globalpick .m-loading")._$style("display", "none");
                t(".m-docfoot")._$style("display", "block");
                a.show({
                    type: "error",
                    message: i,
                    duration: 2e3,
                    singleMsg: !0
                });
                setTimeout(function () {
                    window.scrollBy(0, -1);
                    this.__globalPick.__loading = !1
                }._$bind(this), 2500)
            }._$bind(this)
        };
        o("/home.html", n)
    };
    pro.__fireScrollEvt = function () {
        return n.throttle(function () {
            e._$dispatchEvent(window, "scroll")
        }, 80)
    }();
    s._$$IndexModule._$allocate()
}, 1, 2, 3, 4, 73, 7, 92, 93, 71, 54, 235, 40, 87, 94, 6, 82);
//# sourceMappingURL=./s/pt_pages_index_index.map