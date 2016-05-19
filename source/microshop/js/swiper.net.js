;;if (!this.I$) {
    this.I$ = function () {
        var a = {}, b = [],
                c = function () {
                    return !1
                }, d = {},
                e = function (b, c) {
                    return a.toString.call(b) === "[object " + c + "]"
                };
        return function (f, g) {
            var h = d[f],
                    i = e(g, "Function");
            if (null == g || i || (h = g), i) {
                for (var j = [], k = 2, l = arguments.length; l > k; k++) j.push(I$(arguments[k]));
                var m = {};
                j.push.call(j, m, a, c, b);
                var n = g.apply(null, j) || m;
                if (h && e(n, "Object")) if (Object.keys) for (var p, o = Object.keys(n), k = 0, l = o.length; l > k; k++)
                    p = o[k], h[p] = n[p];
                else for (var p in n) h[p] = n[p];
                else h = n
            }
            return h || (h = {}), d[f] = h, h
        }
    }();
};CMPT=1;DEBUG=0;
I$(14,function (_p,_o,_f,_r){
    var _extpro = Function.prototype;
    /**
     * AOP增强操作，增强操作接受一个输入参数包含以下信息
     *
     *  | 参数名称 | 参数类型  | 参数描述 |
     *  | :--     | :--      | :-- |
     *  | args    | Array    | 函数调用时实际输入参数，各增强操作中可以改变值后将影响至后续的操作 |
     *  | value   | Variable | 输出结果 |
     *  | stopped | Boolean  | 是否结束操作，终止后续操作 |
     *
     * @method external:Function#_$aop
     * @param  {Function} arg0 - 前置操作，接受一个输入参数，见描述信息
     * @param  {Function} arg1 - 后置操作，接受一个输入参数，见描述信息
     * @return {Function}        增强后操作函数
     */
    _extpro._$aop = function(_before,_after){
        var _after = _after||_f,
            _before = _before||_f,
            _handler = this;
        return function(){
            var _event = {args:_r.slice.call(arguments,0)};
            _before(_event);
            if (!_event.stopped){
                _event.value = _handler.apply(this,_event.args);
                _after(_event);
            }
            return _event.value;
        };
    };
    /**
     * 绑定接口及参数，使其的调用对象保持一致
     *
     *  ```javascript
     *  var scope = {a:0};
     *
     *  var func = function(a,b){
*      // 第一个参数 ：1
*      console.log(a);
*      // 第二个参数 ： 2
*      consoel.log(b);
*      // 当前this.a ： 0
*      console.log(this.a);
*  };
     *
     *  func._$bind(scope,"1")(2);
     *  ```
     *
     * @method external:Function#_$bind
     * @see    external:Function#_$bind2
     * @param  {Object} arg0 - 需要保持一致的对象，null表示window对象，此参数外的其他参数作为绑定参数
     * @return {Function}      返回绑定后的函数
     */
    _extpro._$bind = function() {
        var _args = arguments,
            _object = arguments[0],
            _function = this;
        return function(){
// not use slice for chrome 10 beta and Array.apply for android
            var _argc = _r.slice.call(_args,1);
            _r.push.apply(_argc,arguments);
            return _function.apply(_object||null,_argc);
        };
    };
    /**
     * 绑定接口及参数，使其的调用对象保持一致，
     * 该接口与_$bind接口的差别在于绑定时参数和调用时参数的顺序不一样，
     * _$bind优先传入绑定时参数，_$bind2优先传入调用时参数
     *
     *  ```javascript
     *  var scope = {a:0};
     *
     *  var func = function(a,b){
*      // 第一个参数 ：2
*      console.log(a);
*      // 第二个参数 ： 1
*      consoel.log(b);
*      // 当前this.a ： 0
*      console.log(this.a);
*  };
     *
     *  func._$bind(scope,"1")(2);
     *  ```
     *
     * @method external:Function#_$bind2
     * @see    external:Function#_$bind
     * @param  {Object} arg0 - 需要保持一致的对象，null表示window对象，此参数外的其他参数作为绑定参数
     * @return {Function}      返回绑定后的事件函数
     */
    _extpro._$bind2 = function() {
        var _args = arguments,
            _object = _r.shift.call(_args),
            _function = this;
        return function(){
            _r.push.apply(arguments,_args);
            return _function.apply(_object||null,arguments);
        };
    };
// for compatiable
    var _extpro = String.prototype;
    if (!_extpro.trim){
        _extpro.trim = (function(){
            var _reg = /(?:^\s+)|(?:\s+$)/g;
            return function(){
                return this.replace(_reg,'');
            };
        })();
    }
    if (!this.console){
        this.console = {
            log:_f,
            error:_f
        };
    }
    if (!0){
        NEJ = this.NEJ||{};
// copy object properties
// only for nej compatiable
        NEJ.copy = function(a,b){
            a = a||{};
            b = b||_o;
            for(var x in b){
                if (b.hasOwnProperty(x)){
                    a[x] = b[x];
                }
            }
            return a;
        };
// NEJ namespace
        NEJ = NEJ.copy(
            NEJ,{
                O:_o,R:_r,F:_f,
                P:function(_namespace){
                    if (!_namespace||!_namespace.length){
                        return null;
                    }
                    var _package = window;
                    for(var a=_namespace.split('.'),
                            l=a.length,i=(a[0]=='window')?1:0;i<l;
                        _package=_package[a[i]]=_package[a[i]]||{},i++);
                    return  _package;
                }
            }
        );
        return NEJ;
    }
    return _p;
});
I$(16,function (_p,_o,_f,_r){
    /**
     * 遍历对象
     * @param  {Object}   对象
     * @param  {Function} 迭代回调
     * @param  {Object}   回调执行对象
     * @return {String}   循环中断时的key值
     */
    _p.__forIn = function(_obj,_callback,_this){
        if (!_obj||!_callback){
            return null;
        }
        var _keys = Object.keys(_obj);
        for(var i=0,l=_keys.length,_key,_ret;i<l;i++){
            _key = _keys[i];
            _ret = _callback.call(
                _this||null,
                _obj[_key],_key,_obj
            );
            if (!!_ret){
                return _key;
            }
        }
        return null;
    };
    /**
     * 遍历列表
     * @param  {Array}    列表
     * @param  {Function} 迭代回调
     * @param  {Object}   回调执行对象
     * @return {Void}
     */
    _p.__forEach = function(_list,_callback,_this){
        _list.forEach(_callback,_this);
    };
    /**
     * 集合转数组
     * @param  {Object} 集合
     * @return {Array}  数组
     */
    _p.__col2array = function(_list){
        return _r.slice.call(_list,0);
    };
    /**
     * YYYY-MM-DDTHH:mm:ss.sssZ格式时间串转时间戳
     * @param  {String} 时间串
     * @return {Number} 时间戳
     */
    _p.__str2time = function(_str){
        return Date.parse(_str);
    };
    return _p;
});
I$(17,function (NEJ,_p,_o,_f,_r){
    var _platform  = this.navigator.platform,
        _useragent = this.navigator.userAgent;
    /**
     * 平台判断信息
     *
     * ```javascript
     * NEJ.define([
     *     'base/platform'
     * ],function(_m){
*     var _is = _m._$IS;
*     // 是否MAC系统
*     console.log(_is.mac);
*     // 是否IPhone
*     console.log(_is.iphone);
*     // ...
* });
     * ```
     *
     * @const    module:base/platform._$IS
     * @see      module:base/platform._$is
     * @type     {Object}
     * @property {Boolean} mac     - 是否Mac系统
     * @property {Boolean} win     - 是否windows系统
     * @property {Boolean} linux   - 是否linux系统
     * @property {Boolean} ipad    - 是否Ipad
     * @property {Boolean} iphone  - 是否IPhone
     * @property {Boolean} android - 是否Android系统
     * @property {Boolean} ios     - 是否IOS系统
     * @property {Boolean} tablet  - 是否平板
     * @property {Boolean} desktop - 是否桌面系统
     */
    var _is = {
        mac     : _platform,
        win     : _platform,
        linux   : _platform,
        ipad    : _useragent,
        ipod    : _useragent,
        iphone  : _platform,
        android : _useragent
    };
    _p._$IS = _is;
    for(var x in _is){
        _is[x] = new RegExp(x,'i').test(_is[x]);
    }
    _is.ios = _is.ipad||_is.iphone||_is.ipod;
    _is.tablet = _is.ipad;
    _is.desktop = _is.mac||_is.win||(_is.linux&&!_is.android);
    /**
     * 判断是否指定平台
     *
     * ```javascript
     * NEJ.define([
     *     'base/platform'
     * ],function(_m){
*     // 是否MAC系统
*     console.log(_m._$is('mac'));
*     // 是否iphone
*     console.log(_m._$is('iphone'));
*     // ...
* });
     * ```
     *
     * @method module:base/platform._$is
     * @see    module:base/platform._$IS
     * @param  {String} arg0 - 平台名称
     * @return {Boolean}       是否指定平台
     */
    _p._$is = function(_platform){
        return !!_is[_platform];
    };
// parse kernel information
    /**
     * 引擎内核信息
     *
     * ```javascript
     * NEJ.define([
     *     'base/platform'
     * ],function(_m){
*     var _kernel = _m._$KERNEL;
*     // 打印平台信息
*     console.log(_kernel.engine);
*     console.log(_kernel.release);
*     console.log(_kernel.browser);
*     console.log(_kernel.version);
* });
     * ```
     *
     * @const    module:base/platform._$KERNEL
     * @type     {Object}
     * @property {String} engine  - 布局引擎，trident/webkit/gecko/presto...
     * @property {Number} release - 布局引擎版本
     * @property {String} browser - 浏览器名称，ie/chrome/safari/opera/firefox/maxthon...
     * @property {Number} version - 浏览器版本
     * @property {Object} prefix  - 平台前缀，html5/css3 attribute/method/constructor
     */
    var _kernel = {
        engine:'unknow',
        release:'unknow',
        browser:'unknow',
        version:'unknow',
        prefix:{css:'',pro:'',clz:''}
    };
    _p._$KERNEL  = _kernel;
    if (/msie\s+(.*?);/i.test(_useragent)||
        /trident\/.+rv:([\d\.]+)/i.test(_useragent)){
        _kernel.engine  = 'trident';
        _kernel.browser = 'ie';
        _kernel.version = RegExp.$1;
        _kernel.prefix  = {css:'ms',pro:'ms',clz:'MS',evt:'MS'};
// 4.0-ie8 5.0-ie9 6.0-ie10 7.0-ie11
// adjust by document mode setting in develop toolbar
        var _test = {6:'2.0',7:'3.0',8:'4.0',9:'5.0',10:'6.0',11:'7.0'};
        _kernel.release = _test[document.documentMode]||
        _test[parseInt(_kernel.version)];
    }else if(/webkit\/?([\d.]+?)(?=\s|$)/i.test(_useragent)){
        _kernel.engine  = 'webkit';
        _kernel.release = RegExp.$1||'';
        _kernel.prefix  = {css:'webkit',pro:'webkit',clz:'WebKit'};
    }else if(/rv\:(.*?)\)\s+gecko\//i.test(_useragent)){
        _kernel.engine  = 'gecko';
        _kernel.release = RegExp.$1||'';
        _kernel.browser = 'firefox';
        _kernel.prefix  = {css:'Moz',pro:'moz',clz:'Moz'};
        if (/firefox\/(.*?)(?=\s|$)/i.test(_useragent))
            _kernel.version = RegExp.$1||'';
    }else if(/presto\/(.*?)\s/i.test(_useragent)){
        _kernel.engine  = 'presto';
        _kernel.release = RegExp.$1||'';
        _kernel.browser = 'opera';
        _kernel.prefix  = {css:'O',pro:'o',clz:'O'};
        if (/version\/(.*?)(?=\s|$)/i.test(_useragent))
            _kernel.version = RegExp.$1||'';
    }
    if (_kernel.browser=='unknow'){
        var _test = ['chrome','maxthon','safari'];
        for(var i=0,l=_test.length,_name;i<l;i++){
            _name = _test[i]=='safari'?'version':_test[i];
            if (new RegExp(_name+'/(.*?)(?=\\s|$)','i').test(_useragent)){
                _kernel.browser = _test[i];
                _kernel.version = RegExp.$1.trim();
                break;
            }
        }
    }
    /**
     * 引擎特性支持信息
     *
     * ```javascript
     * NEJ.define([
     *     'base/platform'
     * ],function(_m){
*     var _support = _m._$SUPPORT;
*     // 打印平台是否支持CSS3 3D特效
*     console.log(_support.css3d);
* });
     * ```
     * @const    module:base/platform._$SUPPORT
     * @see      module:base/platform._$support
     * @type     {Object}
     * @property {Boolean} css3d  - 是否支持CSS3 3D
     */
    _p._$SUPPORT = {};
    /**
     * 判断平台是否支持指定特性
     *
     * ```javascript
     * NEJ.define([
     *     'base/platform'
     * ],function(_m){
*     // 是否支持CSS3 3D特效
*     console.log(_m._$support('css3d'));
* });
     * ```
     *
     * @method module:base/platform._$support
     * @see    module:base/platform._$SUPPORT
     * @param  {String} arg0 - 特性标识
     * @return {Boolean}       是否支持指定特性
     */
    _p._$support = function(_feature){
        return !!_p._$SUPPORT[_feature];
    };
    if (CMPT){
        NEJ.copy(NEJ.P('nej.p'),_p);
    }
    return _p;
},14);
I$(15,function(_h,_m,_p,_o,_f,_r){var _k_ = (CMPT?NEJ.P("nej.p"):arguments[1])._$KERNEL;if (_k_.engine=='trident'&&_k_.release<='4.0'){(function (){
    /**
     * 遍历对象
     * @param  {Object}   对象
     * @param  {Function} 迭代回调
     * @param  {Object}   回调执行对象
     * @return {String}   循环中断时的key值
     */
    _h.__forIn = function(_obj,_callback,_this){
        if (!_obj||!_callback){
            return;
        }
// iterate
        var _ret;
        for(var x in _obj){
            if (!_obj.hasOwnProperty(x)) continue;
            _ret = _callback.call(_this,_obj[x],x,_obj);
            if (!!_ret){
                return x;
            }
        }
    };
    /**
     * 遍历列表
     * @param  {Array}    列表
     * @param  {Function} 迭代回调
     * @param  {Object}   回调执行对象
     * @return {Void}
     */
    _h.__forEach = function(_list,_callback,_this){
        for(var i=0,l=_list.length;i<l;i++){
            _callback.call(_this,_list[i],i,_list);
        }
    };
    /**
     * 集合转数组
     * @param  {Object} 集合
     * @return {Array}  数组
     */
    _h.__col2array = function(_list){
        var _result = [];
        if (!!_list&&!!_list.length){
            for(var i=0,l=_list.length;i<l;i++){
                _result.push(_list[i]);
            }
        }
        return _result;
    };
    /**
     * YYYY-MM-DDTHH:mm:ss.sssZ格式时间串转时间戳
     * @param  {String} 时间串
     * @return {Number} 时间戳
     */
    _h.__str2time = (function(){
        var _reg = /-/g;
        return function(_str){
// only support YYYY/MM/DDTHH:mm:ss
            return Date.parse(_str.replace(_reg,'/').split('.')[0]);
        };
    })();
})();};return _h;
},16,17);
I$(1,function (NEJ,_u,_p,_o,_f,_r){
    /**
     * 定义类，通过此api定义的类具有以下特性：
     *
     * * {@link external:Function#_$extend|_$extend}作为类的静态扩展方法
     * * __init作为类的初始化函数
     * * __super作为子类调用父类的同名函数
     *
     * ```javascript
     * NEJ.define([
     *     'base/klass'
     * ],function(k,p){
*     // 定义类A
*     p.A = k._$klass();
*     var pro = A.prototype;
*     // 初始化
*     pro.__init = function(){
*          // do init
*     };
*     // 类接口
*     pro.__doSomething = function(a){
*         // TODO something
*     };
*
*     return p;
* });
     * ```
     *
     * ```javascript
     * NEJ.define([
     *     'base/klass',
     *     '/path/to/class/a.js'
     * ],function(k,a,p){
*     // 定义类B，并继承自A
*     p.B = k._$klass();
*     var pro = B._$extend(a.A);
*     // 初始化
*     pro.__init = function(){
*         // 调用A的初始化逻辑
*         this.__super();
*         // TODO B的初始化逻辑
*     };
*     // 类接口
*     pro.__doSomething = function(a){
*         // 调用A的__doSomething接口
*         this.__super(a);
*         // TODO B的逻辑
*     };
*
*     return p;
* });
     * ```
     *
     * @method module:base/klass._$klass
     * @see    external:Function#_$extend
     * @return {Function} 返回定义的类
     */
    _p._$klass = (function(){
        var _isNotFunction = function(){
            return _o.toString.call(arguments[0])!=='[object Function]';
        };
        var _doFindIn = function(_method,_klass){
            while(!!_klass){
                var _pro = _klass.prototype,
                    _key = _u.__forIn(_pro,function(v){
                        return _method===v;
                    });
                if (_key!=null){
                    return {
                        name:_key,
                        klass:_klass
                    };
                }
                _klass = _klass._$super;
            }
        };
        return function(){
// class constructor
            var _Klass = function(){
                return this.__init.apply(this,arguments);
            };
            _Klass.prototype.__init = _f;
            /**
             * 子类继承父类
             *
             * ```javascript
             * NEJ.define([
             *     'base/klass'
             * ],function(k,p){
*     // 定义类A
*     p.A = k._$klass();
*     var pro = A.prototype;
*     // 初始化
*     pro.__init = function(){
*          // do init
*     };
*     // 类接口
*     pro.__doSomething = function(a){
*         // TODO something
*     };
*
*     return p;
* });
             * ```
             *
             * ```javascript
             * NEJ.define([
             *     'base/klass',
             *     '/path/to/class/a.js'
             * ],function(k,a,p){
*     // 定义类B，并继承自A
*     p.B = k._$klass();
*     var pro = B._$extend(a.A);
*     // 初始化
*     pro.__init = function(){
*         // 调用A的初始化逻辑
*         this.__super();
*         // TODO B的初始化逻辑
*     };
*     // 类接口
*     pro.__doSomething = function(a){
*         // 调用A的__doSomething接口
*         this.__super(a);
*         // TODO B的逻辑
*     };
*
*     return p;
* });
             * ```
             *
             * @method external:Function#_$extend
             * @see    module:base/klass._$klass
             * @param  {Function} arg0 - 父类
             * @param  {Boolean}  arg1 - 是否拷贝父类的静态方法，默认拷贝父类静态方法
             * @return {Object}          扩展类的prototype对象
             */
            _Klass._$extend = function(_super,_static){
                if (_isNotFunction(_super)){
                    return;
                }
// for static method
                var _this = this;
                if (_static!==!1){
                    _u.__forIn(_super,function(v,k){
                        if (!_isNotFunction(v)){
                            _this[k] = v;
                        }
                    });
                }
// do inherit
                this._$super = _super;
                var _parent = function(){};
                _parent.prototype = _super.prototype;
                this.prototype = new _parent();
                this.prototype.constructor = this;
// for super method call
                var _stack = [],
                    _phash = {};
                var _doUpdateCache = function(_method,_klass){
                    var _result = _doFindIn(_method,_klass);
                    if (!_result) return;
// save state
                    if (_stack[_stack.length-1]!=_result.name){
                        _stack.push(_result.name);
                    }
                    _phash[_result.name] = _result.klass._$super;
                    return _result.name;
                };
                this.prototype.__super = function(){
                    var _name = _stack[_stack.length-1],
                        _method = arguments.callee.caller;
                    if (!_name){
                        _name = _doUpdateCache(_method,this.constructor);
                    }else{
                        var _parent = _phash[_name].prototype;
// switch caller name
                        if (!_parent.hasOwnProperty(_method)||
                            _method!=_parent[_name]){
                            _name = _doUpdateCache(_method,this.constructor);
                        }else{
                            _phash[_name] = _phash[_name]._$super;
                        }
                    }
// call parent method
                    var _ret = _phash[_name].prototype[_name].apply(this,arguments);
// exit super
                    if (_name==_stack[_stack.length-1]){
                        _stack.pop();
                        delete _phash[_name];
                    }
                    return _ret;
                };
                if (CMPT){
                    var _pro = this.prototype;
                    _pro.__supInit      = _pro.__super;
                    _pro.__supReset     = _pro.__super;
                    _pro.__supDestroy   = _pro.__super;
                    _pro.__supInitNode  = _pro.__super;
                    _pro.__supDoBuild   = _pro.__super;
                    _pro.__supOnShow    = _pro.__super;
                    _pro.__supOnHide    = _pro.__super;
                    _pro.__supOnRefresh = _pro.__super;
                    this._$supro = _super.prototype;
                }
                return this.prototype;
            };
            return _Klass;
        };
    })();
    if (CMPT){
        NEJ.C = _p._$klass;
        NEJ.copy(this.NEJ,NEJ);
    }
    return _p;
},14,15);
I$(2,function (NEJ,_h,_p,_o,_f,_r){
    /*
     * 查看数据是否指定类型
     * @param  {Variable} 数据
     * @param  {String}   类型
     * @return {Boolean}  是否指定类型
     */
    var _isTypeOf = function(_data,_type){
        try{
            _type = _type.toLowerCase();
            if (_data===null) return _type=='null';
            if (_data===undefined) return _type=='undefined';
            return _o.toString.call(_data).toLowerCase()=='[object '+_type+']';
        }catch(e){
            return !1;
        }
    };
    /**
     * 判断是否函数类型
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回false
*     var is = _u._$isFunction(123);
*     // 返回true
*     var is = _u._$isFunction(function(){});
* });
     * ```
     *
     * @method module:base/util._$isFunction
     * @param  {Variable} arg0 - 待检测类型的数据
     * @return {Boolean}         是否函数类型
     */
    _p._$isFunction = function(_data){
        return _isTypeOf(_data,'function');
    };
    /**
     * 判断是否字符串
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回false
*     var is = _u._$isString(123);
*     // 返回true
*     var is = _u._$isString("123");
* });
     * ```
     *
     * @method module:base/util._$isString
     * @param  {Variable} arg0 - 待检测类型的数据
     * @return {Boolean}         是否字符串
     */
    _p._$isString = function(_data){
        return _isTypeOf(_data,'string');
    };
    /**
     * 判断是否数字
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回false
*     var is = _u._$isNumber("123");
*     // 返回true
*     var is = _u._$isNumber(123);
*     var is = _u._$isNumber(-123);
*     var is = _u._$isNumber(Number.MAX_VALUE);
* });
     * ```
     *
     * @method module:base/util._$isNumber
     * @param  {Variable} arg0 - 待检测类型的数据
     * @return {Boolean}         是否数值类型
     */
    _p._$isNumber = function(_data){
        return _isTypeOf(_data,'number');
    };
    /**
     * 判断是否布尔值
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回false
*     var is = _u._$isBoolean(0);
*     // 返回true
*     var is = _u._$isBoolean(false);
* });
     * ```
     *
     * @method module:base/util._$isBoolean
     * @param  {Variable} arg0 - 待检测类型的数据
     * @return {Boolean}         是否布尔值
     */
    _p._$isBoolean = function(_data){
        return _isTypeOf(_data,'boolean');
    };
    /**
     * 判断是否日期
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回false
*     var is = _u._$isDate(0);
*     // 返回true
*     var is = _u._$isDate(new Date());
* });
     * ```
     *
     * @method module:base/util._$isDate
     * @param  {Variable} arg0 - 待检测类型的数据
     * @return {Boolean}         是否日期
     */
    _p._$isDate = function(_data){
        return _isTypeOf(_data,'date');
    };
    /**
     * 判断是否数组
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回false
*     var is = _u._$isArray(0);
*     // 返回true
*     var is = _u._$isArray([1,2]);
* });
     * ```
     *
     * @method module:base/util._$isArray
     * @param  {Variable} arg0 - 待检测类型的数据
     * @return {Boolean}         是否数组
     */
    _p._$isArray = function(_data){
        return _isTypeOf(_data,'array');
    };
    /**
     * 判断是否对象
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回false
*     var is = _u._$isObject(function(){});
*     // 返回true
*     var is = _u._$isObject({});
*     var is = _u._$isObject({a:"a"});
* });
     * ```
     *
     * @method module:base/util._$isObject
     * @param  {Variable} arg0 - 待检测类型的数据
     * @return {Boolean}         是否对象
     */
    _p._$isObject = function(_data){
        return _isTypeOf(_data,'object');
    };
    /**
     * 计算字符串长度，中文算两个字符
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 字符串长度为5
*     var len = _u._$length('你i他');
* });
     * ```
     *
     * @method module:base/util._$length
     * @param  {String} arg0 - 待计算长度字符串
     * @return {Number}        字符串长度
     */
    _p._$length = (function(){
        var _reg = /[^\x00-\xff]/g;
        return function(_content){
            return (''+(_content||'')).replace(_reg,'**').length;
        };
    })();
    /**
     * 遍历对象
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*       var obj = {a:{id:1,name:'a'},b:{id:2,name:'b'},...};
*
*       // 遍历对象
*       _u._$loop(obj,function(_item,_key){
*           // TODO
*       });
*
*       // 从对象里查找id为2的元素，如果有返回KEY，没有返回null
*       var key = _u._$loop(obj,function(_item){
*           return _item.id==2;
*       });
* });
     * ```
     *
     * @method module:base/util._$loop
     * @see    module:base/util._$forIn
     * @param  {Object}   arg0 - 对象
     * @param  {Function} arg1 - 回调，如果返回true，则中断遍历
     * @param  {Object}   arg2 - 回调函数调用时this对象
     * @return {String}          返回中断时的标识，没有中断则统一返回null
     */
    _p._$loop = function(_obj,_callback,_this){
        if (_p._$isObject(_obj)&&
            _p._$isFunction(_callback)){
            return _h.__forIn.apply(_h,arguments);
        }
        return null;
    };
    /**
     * 线性查找指定项
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     var list = ["你","我","他"];
*     // 返回下标1
*     var index = _u._$indexOf(list,"我");
*     // 没有找到，返回-1
*     var index = _u._$indexOf(list,"他们");
*     // 如果第二个参数是过滤接口，根据接口的规则查找
*     // 以下规则排除第一个下标
*     var index = _u._$indexOf(list,function(_item,_index,_list){
*           return _item==='他';
*     });
* });
     * ```
     *
     * @method module:base/util._$indexOf
     * @param  {Array}    arg0 - 待搜索列表
     * @param  {Variable} arg1 - 指定项，如果为function则表示过滤接口
     * @return {Number}          给定项所在的位置索引，以0开始，没有项返回-1
     */
    _p._$indexOf = function(_list,_item){
        var _filter = _p._$isFunction(_item) ? _item
                : function(_value){return _value===_item;},
            _index  = _p._$forIn(_list,_filter);
        return _index!=null?_index:-1;
    };
    /**
     * 二分法查找指定项
     *
     * 验证函数输入输出说明
     *
     * |      | 类型          | 结果说明 |
     * | :--  | :--      | :-- |
     * | 输入  | Variable | 中间项元素 |
     * | 输出  | Number   | < 0  目标元素在低位区间 |
     * |      |          | = 0  匹配到目标元素 |
     * |      |          | > 0  目标元素在高位区间 |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 二分查找id为2的项的索引值
*     var list = [{id:1,name:'aaa'},{id:2,name:'bbbb'},...];
*     var index = _u._$binSearch(list,function(_item){
*         return _item.id-2;
*     });
* });
     * ```
     *
     * @method module:base/util._$binSearch
     * @param  {Array}    arg0 - 待查找列表
     * @param  {Function} arg1 - 验证函数
     * @return {Number}          找到匹配项索引，找不到返回-1
     */
    _p._$binSearch = (function(){
        var _docheck;
// do binary search
        var _doSearch = function(_list,_low,_high){
            if (_low>_high) return -1;
            var _middle = Math.ceil((_low+_high)/2),
                _result = _docheck(_list[_middle],_middle,_list);
            if (_result==0)
                return _middle;
            if (_result<0)
                return _doSearch(_list,_low,_middle-1);
            return _doSearch(_list,_middle+1,_high);
        };
        return function(_list,_check){
            _docheck = _check||_f;
            return _doSearch(_list,0,_list.length-1);
        };
    })();
    /**
     * 逆序遍历列表，支持中断
     *
     * 回调函数输入输出说明
     *
     * |      | 类型          | 说明 |
     * | :--  | :--      | :-- |
     * | 输入  | Variable | 值 |
     * |      | Number   | 下标 |
     * |      | Array    | 列表对象 |
     * | 输出  | Boolean  | 是否匹配 |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 删除id为3的项，并退出循环
*     var list = [{id:1,name:'aaa'},{id:2,name:'bbbb'},...];
*     _u._$reverseEach(list,function(_item,_index,_list){
*         if (_item.id==3){
*             _list.splice(_index,1);
*             return !0;
*         }
*     });
* });
     * ```
     *
     * @method module:base/util._$reverseEach
     * @see    module:base/util._$forEach
     * @param  {Array}    arg0 - 列表
     * @param  {Function} arg1 - 回调，如果返回true，则中断遍历
     * @param  {Object}   arg2 - 回调函数调用时this对象
     * @return {Number}          返回遍历中断时的索引值，没有中断则返回null
     */
    _p._$reverseEach = function(_list,_callback,_this){
        if (!!_list&&!!_list.length&&_p._$isFunction(_callback)){
            for(var i=_list.length-1;i>=0;i--){
                if (!!_callback.call(_this,_list[i],i,_list)){
                    return i;
                }
            }
        }
        return null;
    };
    /**
     * 正序遍历列表，不支持中断
     *
     * 回调函数输入输出说明
     *
     * |      | 类型          | 说明 |
     * | :--  | :--      | :-- |
     * | 输入  | Variable | 值 |
     * |      | Number   | 下标 |
     * |      | Array    | 列表对象 |
     * | 输出  | Boolean  | 是否匹配 |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     var list = [1,2,3];
*     _u._$forEach(list,function(_item,_index,_list){
*         // TODO somthing
*     });
* });
     * ```
     *
     * @method module:base/util._$forEach
     * @see    module:base/util._$reverseEach
     * @param  {Array}    arg0 - 列表
     * @param  {Function} arg1 - 回调，如果返回true，则中断遍历
     * @param  {Object}   arg2 - 回调函数调用时this对象
     * @return {Void}
     */
    _p._$forEach = function(_list,_callback,_this){
        if (!!_list&&!!_list.length&&
            _p._$isFunction(_callback)){
            if (!_list.forEach){
                _p._$forIn.apply(_p,arguments);
            }else{
                _h.__forEach(_list,_callback,_this);
            }
        }
    };
    /**
     * 遍历列表或对象，如果带length属性，则作为数组遍历，如果要遍历带length属性的对象用_$loop接口，支持中断退出
     *
     * 回调函数输入输出说明
     *
     * |      | 类型          | ���明 |
     * | :--  | :--      | :-- |
     * | 输入  | Variable | 值 |
     * |      | Number   | 下标 |
     * |      | Object_Array | 列表或者集合对象 |
     * | 输出  | Boolean  | 是否匹配 |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*       // 从有序列表里查找id为2的元素，如果有则返回索引，没有返回null
*       var list = [{id:1,name:'a'},{id:2,name:'b'},...];
*       var index = _u._$forIn(list,function(_item){
*           return _item.id==2;
*       });
*
*       // 从对象里查找id为2的元素，如果有返回KEY，没有返回null
*       var obj = {a:{id:1,name:'a'},b:{id:2,name:'b'},...};
*       var key = _u._$forIn(obj,function(_item){
*           return _item.id==2;
*       });
* });
     * ```
     *
     * @method module:base/util._$forIn
     * @param  {Object|Array} arg0 - 列表或者对象
     * @param  {Function}     arg1 - 回调，如果返回true，则中断遍历
     * @param  {Object}       arg2 - 回调函数调用时this对象
     * @return {String|Number}       返回中断时的索引或者标识，没有中断则统一返回null
     */
    _p._$forIn = function(_list,_callback,_this){
        if (!_list||!_p._$isFunction(_callback)){
            return null;
        }
        if (_p._$isNumber(_list.length)){
// list see as array
            for(var i=0,l=_list.length;i<l;i++){
                if (!!_callback.call(_this,_list[i],i,_list)){
                    return i;
                }
            }
        }else if (_p._$isObject(_list)){
// list is object
            return _p._$loop(_list,_callback,_this);
        }
        return null;
    };
    /**
     * 编码字符串，
     * 编码规则对象中r正则表达式参数提取字符串需要编码的内容，
     * 然后使用编码规则对象中的映射表进行替换
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 把字符串99999根据规则9替换成t，结果：ttttt
*     var str = _u._$encode({r:/\d/g,'9':'t'},'99999');
* });
     * ```
     *
     * @method module:base/util._$encode
     * @param  {Object} arg0 - 编码规则
     * @param  {String} arg1 - 待编码的字串
     * @return {String}        编码后的字串
     */
    _p._$encode = function(_map,_content){
        _content = ''+_content;
        if (!_map||!_content){
            return _content||'';
        }
        return _content.replace(_map.r,function($1){
            var _result = _map[!_map.i?$1.toLowerCase():$1];
            return _result!=null?_result:$1;
        });
    };
    /**
     * 编码html代码，'<' -> '&amp;lt;'
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 编码，结果：&amp;lt;a&amp;gt;util&amp;lt;/a&amp;gt;&amp;amp;
*     var str = _u._$escape('<a>util</a>&');
* });
     * ```
     *
     * @method module:base/util._$escape
     * @see    module:base/util._$unescape
     * @param  {String} arg0 - 待编码串
     * @return {String}        编码后的串
     */
    _p._$escape = (function(){
        var _reg = /<br\/?>$/,
            _map = {
                r:/\<|\>|\&|\r|\n|\s|\'|\"/g,
                '<':'&lt;','>':'&gt;','&':'&amp;',' ':'&nbsp;',
                '"':'&quot;',"'":'&#39;','\n':'<br/>','\r':''
            };
        return function(_content){
            _content = _p._$encode(_map,_content);
            return _content.replace(_reg,'<br/><br/>');
        };
    })();
    /**
     * 反编码html代码，'&amp;lt;' -> '<'
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 反编码，结果：<&a>util</a>
*     var str = _u._$unescape('&amp;lt;&amp;amp;a&amp;gt;util&amp;lt;/a&amp;gt;');
* });
     * ```
     *
     * @method module:base/util._$unescape
     * @see    module:base/util._$escape
     * @param  {String} arg0 - 待反编码串
     * @return {String}        反编码后的串
     */
    _p._$unescape = (function(){
        var _map = {r:/\&(?:lt|gt|amp|nbsp|#39|quot)\;|\<br\/\>/gi,'&lt;':'<','&gt;':'>','&amp;':'&','&nbsp;':' ','&#39;':"'",'&quot;':'"','<br/>':'\n'};
        return function(_content){
            return _p._$encode(_map,_content);
        };
    })();
    /**
     * 格式化时间，yyyy|yy|MM|cM|eM|M|dd|d|HH|H|mm|ms|ss|m|s|w
     *
     * 各标识说明：
     *
     * | 标识  | 说明 |
     * | :--  | :-- |
     * | yyyy | 四位年份，如2001 |
     * | yy   | 两位年费，如01 |
     * | MM   | 两位月份，如08 |
     * | M    | 一位月份，如8 |
     * | dd   | 两位日期，如09 |
     * | d    | 一位日期，如9 |
     * | HH   | 两位小时，如07 |
     * | H    | 一位小时，如7 |
     * | mm   | 两位分钟，如03 |
     * | m    | 一位分钟，如3 |
     * | ss   | 两位秒数，如09 |
     * | s    | 一位秒数，如9 |
     * | ms   | 毫秒数，如234 |
     * | w    | 中文星期几，如一 |
     * | ct   | 12小时制中文后缀，上午/下午 |
     * | et   | 12小时制英文后缀，A.M./P.M. |
     * | cM   | 中文月份，如三 |
     * | eM   | 英文月份，如Mar |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 根据格式输出时间，比如:2012-01-11,连接符可自定义
*     var str = _u._$format(new Date(),'yyyy-MM-dd');
* });

    /**
     * 日期字符串转日期对象
     *
     * 字符串日期格式同ECMA规范定义：YYYY-MM-DDTHH:mm:ss.sssZ
     *
     * 各标识说明：
     *
     * | 标识 | 说明 |
     * | :--  | :-- |
     * | YYYY | 四位年份，0000-9999，如2001 |
     * | -    | 年月日分隔符 |
     * | MM   | 两位月份，01-12，如03 |
     * | DD   | 两位日期，01-31，如07 |
     * | T    | 时间起始标识 |
     * | HH   | 两位小时，00-24，如05 |
     * | :    | 时分秒分隔符 |
     * | mm   | 两位分钟，00-59，如30 |
     * | ss   | 两位秒数，00-59，如08 |
     * | .    | 秒/毫秒分隔符 |
     * | sss  | 三位毫秒数，000-999，如004 |
     * | Z    | 时区偏移 |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 输入YYYY-MM-DDTHH:mm:ss.sssZ格式字符串，生成日期对象
*     var date = _u._$var2date('2013-07-29T13:12:45.300');
*
*     // 输入YYYY-MM-DDTHH:mm:ss格式字符串，生成日期对象
*     var date = _u._$var2date('2013-07-29T13:12:45');
*
*     // 输入YYYY-MM-DD格式字符串，生成日期对象
*     var date = _u._$var2date('2013-07-29');
* });
     * ```
     *
     * @method module:base/util._$var2date
     * @param  {String} arg0 - 日期串
     * @return {Date}          日期对象
     */
    _p._$var2date = function(_time){
        var _date = _time;
        if (_p._$isString(_time)){
            _date = new Date(
                _h.__str2time(_time)
            );
        }
        if (!_p._$isDate(_date)){
            _date = new Date(_time);
        }
        return _date;
    };
    /**
     * 浮点数值保留指定位数小数点
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 保留2位小数，返回3.14
*     var value = _u._$fixed(3.14159,2);
* });
     * ```
     *
     * @method module:base/util._$fixed
     * @param  {Float}  arg0 - 浮点数
     * @param  {Number} arg1 - 小数位
     * @return {Number}        浮点数
     */
    _p._$fixed = function(_float,_fraction){
        return parseFloat(new Number(_float).toFixed(_fraction));
    };
    /**
     * 相对路径转绝对路径
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 相对路径../a/b.html转绝对路径http://a.b.com:8010/a/b.html
*     var url = _u._$absolute(
*         '../a/b.html',
*         'http://a.b.com:8010/z/'
*     );
* });
     * ```
     *
     * @method module:base/util._$absolute
     * @param  {String} arg0 - 相对路径
     * @param  {String} arg1 - 绝对路径ROOT，必须以http://开始，默认为location目录
     * @return {String}        绝对路径地址
     */
    _p._$absolute = (function(){
        var _reg0 = /([^\/:])\/.*$/,
            _reg1 = /\/[^\/]+$/,
            _reg2 = /[#\?]/,
            _base = location.href.split(/[?#]/)[0],
            _anchor = document.createElement('a');
        var _isAbsolute = function(_uri){
            return (_uri||'').indexOf('://')>0;
        };
        var _doFormat = function(_uri){
            return (_uri||'').split(_reg2)[0]
                .replace(_reg1,'/');
        };
        var _doMergeURI = function(_uri,_root){
// for /a/b/c
            if (_uri.indexOf('/')==0)
                return _root.replace(_reg0,'$1')+_uri;
// for a/b or ./a/b or ../a/b
            return _doFormat(_root)+_uri;
        };
        _base = _doFormat(_base);
        return function(_uri,_root){
            _uri = (_uri||'').trim();
            if (!_isAbsolute(_root))
                _root = _base;
            if (!_uri) return _root;
            if (_isAbsolute(_uri))
                return _uri;
            _uri = _doMergeURI(_uri,_root);
            _anchor.href = _uri;
            _uri = _anchor.href;
            return _isAbsolute(_uri) ? _uri :
                _anchor.getAttribute('href',4); // ie6/7
        };
    })();
    /**
     * 从URL地址中提取源信息
     *
     * * http://a.b.com:8080/a/b/ -> http://a.b.com:8080
     * * /a/b ->
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 提取url地址的源信息
*     // 返回http://a.b.com:8080
*     var origin = _u._$url2origin("http://a.b.com:8080/a/b/");
* });
     * ```
     *
     * @method module:base/util._$url2origin
     * @param  {String} arg0 - URL地址
     * @return {String}        源信息
     */
    _p._$url2origin = (function(){
        var _reg = /^([\w]+?:\/\/.*?(?=\/|$))/i;
        return function(_url){
            if (_reg.test(_url||''))
                return RegExp.$1.toLowerCase();
            return '';
        };
    })();
    /**
     * key-value字符串转对象
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     var str = "abc=abc,123=123";
*     // 返回对象{abc:"abc",123:"123"}
*     var obj = _u._$string2object(_str,",");
* });
     * ```
     *
     * @method module:base/util._$string2object
     * @see    module:base/util._$object2string
     * @param  {String}        arg0 - 待处理数据
     * @param  {String|RegExp} arg1 - 分隔符
     * @return {Object}               转换后对象
     */
    _p._$string2object = function(_string,_split){
        var _obj = {};
        _p._$forEach(
            (_string||'').split(_split),
            function(_name){
                var _brr = _name.split('=');
                if (!_brr||!_brr.length) return;
                var _key = _brr.shift();
                if (!_key) return;
                _obj[decodeURIComponent(_key)] =
                    decodeURIComponent(_brr.join('='));
            }
        );
        return _obj;
    };
    /**
     * key-value对象转成key=value对后用分隔符join
     *
     * 对象中不同类型的取值规则如下：
     *
     * | 类型            |  取值规则 |
     * | :--       | :-- |
     * | Function  |  过滤掉，不输出 |
     * | Date      |  转成时间戳，getTime取值 |
     * | Array     |  值用逗号分隔，如[1,2,3] -> 1,2,3 |
     * | Object    |  使用JSON转成字符串 |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回字符串 abc=abc,123=123
*     var obj = {
*         abc:"abc",
*         123:"123"
*     };
*     var str = _u._$object2string(obj);
*
*     // 返回字符串
*     // a=1871406603152186&b=1,2,3&d={"a":"a","b":"b"}&e=e&f=1&g=true
*     var obj = {
*         a:new Date,
*         b:[1,2,3],
*         c:function(){},
*         d:{a:'a',b:'b'},
*         e:'e',
*         f:1,
*         g:true
*     };
*     var str = _u._$object2string(obj,'&');
* });
     * ```
     *
     * @method module:base/util._$object2string
     * @see    module:base/util._$string2object
     * @param  {Object}  arg0 - 对象
     * @param  {String}  arg1 - 分隔符，默认为逗号
     * @param  {Boolean} arg2 - 是否编码
     * @return {String}         key-value串
     */
    _p._$object2string = function(_object,_split,_encode){
        if (!_object) return '';
        var _arr = [];
        _p._$loop(
            _object,function(_value,_key){
                if (_p._$isFunction(_value)){
                    return;
                }
                if (_p._$isDate(_value)){
                    _value = _value.getTime();
                }else if(_p._$isArray(_value)){
                    _value = _value.join(',');
                }else if(_p._$isObject(_value)){
                    _value = JSON.stringify(_value);
                }
                if (!!_encode){
                    _value = encodeURIComponent(_value);
                }
                _arr.push(encodeURIComponent(_key)+'='+_value);
            }
        );
        return _arr.join(_split||',');
    };
    /**
     * 查询串转对象
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回对象{abc:"abc",123:"123"}
*     var obj = _u._$query2object("abc=abc&123=123");
* });
     * ```
     *
     * @method module:base/util._$query2object
     * @see    module:base/util._$object2query
     * @see    module:base/util._$string2object
     * @param  {String} arg0 - 查询串
     * @return {Object}        转换出来的对象
     */
    _p._$query2object = function(_query){
        return _p._$string2object(_query,'&');
    };
    /**
     * 对象转查询串
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回对象123=123&abc=abc
*     var query = _u._$object2query({abc:"abc",123:"123"});
* });
     * ```
     *
     * @method module:base/util._$object2query
     * @see    module:base/util._$query2object
     * @see    module:base/util._$object2string
     * @param  {Object} arg0 - 对象
     * @return {String}        查询串
     */
    _p._$object2query = function(_object){
        return _p._$object2string(_object,'&',!0);
    };
    /**
     * 集合转数组，集合具有length属性
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 返回数组['1','2','3']
*     var map = {0:'0',1:'1',2:'2',length:3};
*     var arr = _u._$object2array(map);
*
*     // 多用于对节点集合的转换
*     var nodes = document.body.childNodes;
*     var arr = _u._$object2array(nodes);
* });
     * ```
     *
     * @method module:base/util._$object2array
     * @see    module:base/util._$array2object
     * @param  {Object} arg0 - 集合，必须有length属性
     * @return {Array}         数组
     */
    _p._$object2array = function(_object){
        return _h.__col2array(_object);
    };
    /**
     * 数组转对象，将列表中元素按照指定KEY组成对象<br/>
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 输出结果为 {2:{id:2,name:'b'},...}
*     var arr = [{id:1,name:'a'},{id:2,name:'b'},...];
*     var obj = _u._$array2object(
*         arr,function(_item){
*             // 过滤name为a的项
*             if (_item.name=='a'){
*                 return;
*             }
*             // 组对象的KEY用每项的id
*             return _item.id;
*         }
*     );
*
*     // 默认使用每项的值组对象
*     var brr = ['a','b','c',...];
*     // 输出 {a:'a',b:'b',c:'c',...}
*     var obj = _u._$array2object(brr);
* });
     * ```
     *
     * @method module:base/util._$array2object
     * @see    module:base/util._$object2array
     * @param  {Array}    arg0 - 列表
     * @param  {Function} arg1 - 过滤函数，返回每一项的KEY，没有返回则过滤当前项
     * @return {Object}   对象
     */
    _p._$array2object = function(_list,_filter){
        var _result = {};
        _p._$forEach(
            _list,function(_item){
                var _key = _item;
                if (!!_filter){
                    _key = _filter(_item);
                }
                if (_key!=null){
                    _result[_key] = _item;
                }
            }
        );
        return _result;
    };
    /**
     * 格式化数字为指定位数，不足位数前面用0补足
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 2    -> 002
*     // 22   -> 022
*     // 222  -> 222
*     // 2222 -> 2222
*     var str = _u._$number2string(2,3);
* });
     * ```
     *
     * @method module:base/util._$number2string
     * @param  {Number} arg0 - 数值
     * @param  {Number} arg1 - 位数，至少1位
     * @return {String}        格式化后字符串
     */
    _p._$number2string = function(_number,_limit){
        var _len1 = (''+_number).length,
            _len2 = Math.max(1,parseInt(_limit)||0),
            _delta = _len2-_len1;
        if (_delta>0){
            _number = new Array(_delta+1).join('0')+_number;
        }
        return ''+_number;
    };
    /**
     * 安全删除属性，
     * 部分浏览器（如低版本IE）禁止直接delete节点上的属性
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 节点上保存的数据
*     _node.data = {a:'aaaaa',b:'bbbbb'};
*     _node.test = 'aaaaa';
*
*     // 删除单个属性
*     _u._$safeDelete(_node,'test');
*     // 批量删除
*     _u._$safeDelete(_node,['test','data']);
* });

    /**
     * 随机一个字符串
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 可能返回"13d1r1dt2"
*     var seed = _u._$randString(9);
* });
     * ```
     *
     * @method module:base/util._$randString
     * @param  {String} arg0 - 字符串长度
     * @return {String}        随机字符串
     */
    _p._$randString = (function(){
        var _chars = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXTZabcdefghiklmnopqrstuvwxyz';
        return function(_length){
            _length = _length||10;
            var _result = [];
            for(var i=0,_rnum;i<_length;++i){
                _rnum = Math.floor(Math.random()*_chars.length);
                _result.push(_chars.charAt(_rnum));
            }
            return _result.join('');
        };
    })();
    /**
     * 随机生成一个给定范围的整数
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 可能返回3
*     var seed = _u._$randNumber(0,9);
* });
     * ```
     *
     * @method module:base/util._$randNumber
     * @see    module:base/util._$randNumberString
     * @param  {Number} arg0 - 小区间，包含
     * @param  {Number} arg1 - 大区间，不包含
     * @return {Number}        随机整数
     */
    _p._$randNumber = function(_min,_max){
        return Math.floor(Math.random()*(_max-_min)+_min);
    };
    /**
     * 随机生成一个全部为数字的字符串
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 可能返回123456789
*     var seed = _u._$randNumberString(9);
* });
     * ```
     *
     * @deprecated
     * @method module:base/util._$randNumberString
     * @see    module:base/util._$randNumber
     * @see    module:base/util._$uniqueID
     * @param  {Number} arg0 - 随机字符串的长度[1,30]
     * @return {String}        随机生成的字符串
     */
    _p._$randNumberString = function(_length){
        _length = Math.max(0,Math.min(_length||8,30));
        var _min = Math.pow(10,_length-1),_max = _min*10;
        return _p._$randNumber(_min,_max).toString();
    };
    /**
     * 生成系统中的唯一标识，每次调用均生成一个新的标识
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_p){
*    // 可能返回123456789
*    var _id1 = _p._$uniqueID(),
*        _id2 = _p._$uniqueID();
*    // _id1 != _id2
* });
     * ```
     *
     * @method module:base/util._$uniqueID
     * @return {String} 唯一标识
     */
    _p._$uniqueID = (function(){
        var _seed = +new Date;
        return function(){
            return ''+(_seed++);
        };
    })();
    /**
     * 读取上下文中指定名字空间的值
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     var obj = {
*         a:{
*             b:{
*                 c:{
*                     d:'ddddd'
*                 }
*             }
*         }
*     };
*     // 输出 ddddd
*     var value = _u._$query(obj,'a.b.c.d');
*     // 输出 undefined
*     var value = _u._$query(null,'a.b.c.d');
* });
     * ```
     *
     * @method module:base/util._$query
     * @param  {Object} arg0 - 上下文
     * @param  {String} arg1 - 名字空间
     * @return {Varaible}      查询到的值
     */
    _p._$query = function(_context,_namespace){
        _context = _context||_o;
        var _arr = (_namespace||'').split('.');
        for(var i=0,l=_arr.length;i<l;i++){
            _context = _context[_arr[i]];
            if (!_context) break;
        }
        return _context;
    };
    /**
     * 合并数据，同名属性右侧覆盖左侧，
     * 最后一个如果是函数则用做数据过滤，
     * 第一个参数作为合并数据结果集对象，如果为空则新建对象
     *
     * 过滤接口输入输出说明
     *
     * |      | 类型          | 说明 |
     * | :--  | :--      | :-- |
     * | 输入  | Variable | 值 |
     * |      | String   | 键 |
     * | 输出  | Boolean  | 是否过滤 |
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 合并多个数据至obj0中
*     var obj0 = {a:0,b:1},
*         obj1 = {a:"a",b:"b",c:"c"},
*         obj2 = {c:"c",d:"d",e:"f"},
*         ... ;
*     var obj = _u._$merge(obj0,obj1,obj2,...);
*
*     // 带过滤接口合并
*     // 阻止a属性的覆盖
*     var obj = _u._$merge(
*         obj0,obj1,obj2,...,
*         function(_value,_key){
*             return _key=='a';
*         }
*     );
* });
     * ```
     *
     * @method module:base/util._$merge
     * @see    module:base/util._$fetch
     * @param  {Object}   arg0 - 原始对象
     * @param  {Object}   arg1 - 待拷贝对象
     * @param  {Function} arg2 - 过滤接口
     * @return {Object}          拷贝后对象
     */
    _p._$merge = function(){
        var _last = arguments.length-1,
            _filter = arguments[_last];
// check filter function for last args
        if (_p._$isFunction(_filter)){
            _last -= 1;
        }else{
            _filter = _f;
        }
// args0 as result
        var _result = arguments[0]||{};
// merge
        for(var i=1;i<=_last;i++){
            _p._$loop(arguments[i],function(v,k){
                if (!_filter(v,k)){
                    _result[k] = v;
                }
            });
        }
        return _result;
    };
    /**
     * 根据原始对象属性，从目标对象提取非空值
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     var obj0 = {a:0,b:1},
*         obj1 = {a:"a",b:"b",c:"c"};
*     // 根据obj0的属性,从obj1拷贝非null属性到obj0中
*     // 结果是obj0.a = "a",obj.b = "b",没有拷贝c属性;
*     var obj = _u._$fetch(obj0,obj1);
* });
     * ```
     *
     * @method module:base/util._$fetch
     * @see    module:base/util._$merge
     * @param  {Object} arg0 - 原始对象
     * @param  {Object} arg1 - 目标对象
     * @return {Object}        合并后的对象
     */
    _p._$fetch = function(_object,_config){
        if (!!_config){
            _p._$loop(_object,function(v,k,m){
                var _value = _config[k];
                if (_value!=null){
                    m[k] = _value;
                }
            });
        }
        return _object;
    };
    /**
     * 判断对象自生是否包含元素
     *
     * ```javascript
     * NEJ.define([
     *     'base/util'
     * ],function(_u){
*     // 判断空对象是否有属性
*     // 输出 false
*     var has = _u._$hasProperty({});
*
*     // 判断非空对象是否有属性
*     // 输出 true
*     var has = _u._$hasProperty({a:'a',b:'b',c:'c'});
*
*     // 判断空数组是否有属性
*     // 输出 false
*     var has = _u._$hasProperty([]);
*
*     // 判断非空数组是否有属性
*     // 输出 true
*     var has = _u._$hasProperty([1,2,3]);
* });
     * ```
     *
     * @method module:base/util._$hasProperty
     * @param  {Object|Array} arg0 - 对象
     * @return {Boolean}             是否有元素
     */
    _p._$hasProperty = function(_obj){
// for null
        if (!_obj){
            return !1;
        }
// for object with length
        if (_obj.length!=null){
            return _obj.length>0;
        }
// for object
        var _length = 0;
        _p._$loop(_obj,function(){
            _length++;
            return _length>0;
        });
        return _length>0;
    };
    if (CMPT){
        NEJ.Q  = _p._$query;
        NEJ.X  = _p._$merge;
        NEJ.EX = _p._$fetch;
        NEJ.copy(this.NEJ,NEJ);
        NEJ.copy(NEJ.P('nej.u'),_p);
    }
    return _p;
},14,15);


I$(18,function (_u,_p){
    var _cache = {};
    /**
     * 添加可链式调用的接口
     *
     * 添加可链式接口
     * ```javascript
     * NEJ.define([
     *     'base/chain'
     * ],function(_l){
*     var _map = {};
*
*      _map._$api1 = function(){
*          // TODO
*      }
*
*      _map._$api2 = function(){
*          // TODO
*      }
*
*     _l._$merge(_map);
* });
     * ```
     *
     * 使用链式调用接口
     * ```javascript
     * NEJ.define([
     *     '/path/to/api.js',
     *     'util/chain/chainable'
     * ],function(_x,$){
*     // 使用��式调用api
*     $('body > p')._$api1()._$api2();
* });
     * ```
     *
     * @method module:base/chain._$merge
     * @param  {Object} arg0 - 接口集合
     * @return {Void}
     */
    _p._$merge = function(_map){
        _u._$merge(_cache,_map);
    };
    /**
     * 导出链式接口列表
     *
     * @method module:base/chain._$dump
     * @return {Object} 链式接口列表
     */
    _p._$dump = function(){
        return _cache;
    };
    /**
     * 清除链式列表
     *
     * @method module:base/chain._$clear
     * @return {Void}
     */
    _p._$clear = function(){
        _cache = {};
    };
    return _p;
},2);
I$(25,function (_u,_m,_p,_o,_f,_r){
    /**
     * 从DocumentFragment中取指定ID的节点
     * @param  {Document} 文档对象
     * @param  {String}   节点标识
     * @return {Node}     指定标识的节点
     */
    _p.__getElementById = function(_fragment,_id){
        if (!!_fragment.getElementById){
            return _fragment.getElementById(''+_id);
        }
        try{
            return _fragment.querySelector('#'+_id);
        }catch(e){
            return null;
        }
    };
    /**
     * 取节点的子节点列表
     * @param  {Node}  节点ID或者对象
     * @return {Array} 子节点列表
     */
    _p.__getChildren = function(_element){
        return _u._$object2array(_element.children);
    };
    /**
     * 根据类名取节点列表
     * @param  {Node}   节点ID或者对象
     * @param  {String} 类名
     * @return {Array}  节点列表
     */
    _p.__getElementsByClassName = function(_element,_class){
        return _u._$object2array(_element.getElementsByClassName(_class));
    };
    /**
     * 取下一个兄弟节点
     * @param  {Node}  节点对象
     * @return {Node}  节点
     */
    _p.__nextSibling = function(_element){
        return _element.nextElementSibling;
    };
    /**
     * 取上一个兄弟节点
     * @param  {Node}  节点对象
     * @return {Node}  节点
     */
    _p.__previousSibling = function(_element){
        return _element.previousElementSibling;
    };
    /**
     * 设置、获取数据
     * @param {Node}     节点
     * @param {String}   标识
     * @param {Variable} 值
     */
    _p.__dataset = function(_element,_name,_value){
        _element.dataset = _element.dataset||{};
        if (_value!==undefined){
            _element.dataset[_name] = _value;
        }
        return _element.dataset[_name];
    };
    /**
     * 取节点属性值
     * @param  {Node}   节点
     * @param  {String} 属性名
     * @return {String} 属性值
     */
    _p.__getAttribute = function(_element,_name){
        return _element.getAttribute(_name);
    };
    /**
     * 将dom节点转为xml串
     * @param  {Node}   节点
     * @return {String} XML代码
     */
    _p.__serializeDOM2XML = function(_dom){
        return new XMLSerializer().serializeToString(_dom)||'';
    };
    /**
     * 将xml转为dom节点
     * @param  {String} XML代码
     * @return {Node}   节点
     */
    _p.__parseDOMFromXML = function(_xml){
        var _root = new DOMParser()
            .parseFromString(_xml,'text/xml')
            .documentElement;
        return _root.nodeName=='parsererror'?null:_root;
    };
    /**
     * 节点占全屏
     * @param  {Node}   节点
     * @param  {Object} 视窗模型
     * @return {Void}
     */
    _p.__fullScreen = function(){
// use css fixed position
    };
    /**
     * 为节点增加用于盖select/flash等控件的层
     * @param  {Node} 节点
     * @return {Void}
     */
    _p.__mask = function(){
// do nothing
    };
    /**
     * 去除用于盖select/flash等控件的层
     * @param  {Node} 节点
     * @return {Void}
     */
    _p.__unmask = function(){
// do nothing
    };
// variables
    var _ospt = _m._$SUPPORT,
        _opfx = _m._$KERNEL.prefix;
    /**
     * 指定名称是否在配置表中
     * @param  {String}  名称
     * @param  {Object}  配置表
     * @return {Boolean} 是否命中
     */
    _p.__isMatchedName = (function(){
        var _reg = /^([a-z]+?)[A-Z]/;
        return function(_name,_map){
            return !!(_map[_name]||(_reg.test(_name)&&_map[RegExp.$1]));
        };
    })();
    /**
     * 样式名称做前缀增强
     * @param  {String}  名称
     * @return {Boolean} 是否需要前缀增强
     */
    _p.__isNeedPrefixed = (function(){
        var _pmap = _u._$array2object([
            'animation','transform','transition',
            'appearance','userSelect','box','flex','column'
        ]);
        return function(_name){
            return _p.__isMatchedName(_name,_pmap);
        };
    })();
    /**
     * 格式化样式属性名称
     * border-width -> borderWidth
     * @param  {String} 样式样式名
     * @return {String} 格式化后样式名
     */
    _p.__fmtStyleName = (function(){
        var _reg = /-([a-z])/g;
        return function(_name){
            _name = _name||'';
            return _name.replace(_reg,function($1,$2){
                return $2.toUpperCase();
            });
        };
    })();
    /**
     * 针对样式名称做格式化及前缀增强
     * @param  {String} 样式名
     * @return {String} 增强后的样式名
     */
    _p.__getStyleName = (function(){
        var _reg = /^[a-z]/,
            _prefix = _opfx.css||'';
        return function(_name){
            _name = _p.__fmtStyleName(_name);
            if (!_p.__isNeedPrefixed(_name)){
                return _name;
            }
// add prefix
// userSelect -> webkitUserSelect
            return _prefix+_name.replace(_reg,function($1){
                    return $1.toUpperCase();
                });
        };
    })();
    /**
     * 取样式值
     * @param  {String|Node} 节点
     * @param  {String}      样式名称
     * @return {Variable}    样式值
     */
    _p.__getStyleValue = function(_element,_name){
        var _current = window.getComputedStyle(_element,null);
        return _current[_p.__getStyleName(_name)]||'';
    };
    /**
     * 设置样式
     * @param  {String|Node} 节点
     * @param  {String}      样式名称
     * @param  {String}      样式值
     * @return {Void}
     */
    _p.__setStyleValue = function(_element,_name,_value){
        _element.style[_p.__getStyleName(_name)] = _value;
    };
    /**
     * 取样式变换矩阵对象
     * @param  {String}    变换信息
     * @return {CSSMatrix} 变换矩阵对象
     */
    _p.__getCSSMatrix = (function(){
        var _reg0 = /\((.*?)\)/,
            _reg1 = /\s*,\s*/,
            _klss = ['CSSMatrix',_opfx.clz+'CSSMatrix'],
            _list = ['m11','m12','m21','m22','m41','m42'];
// matrix(1,2,3,4,5,6)
// -> {m11:1,m12:2,m21:3,m22:4,m41:5,m42:6}
        var _doParse = function(_matrix){
            var _obj = {};
            if (_reg0.test(_matrix||'')){
// 11,12,21,22,41,42
                _u._$forEach(
                    RegExp.$1.split(_reg1),
                    function(_value,_index){
                        _obj[_list[_index]] = _value;
                    }
                );
            }
            return _obj;
        };
        return function(_matrix){
            var _mtrx;
            _u._$forIn(_klss,function(_name){
                if (!!this[_name]){
                    _mtrx = new this[_name](_matrix||'');
                    return !0;
                }
            });
            return !_mtrx?_doParse(_matrix):_mtrx;
        };
    })();
    /**
     * 注入样式
     * @param  {Node}   样式节点
     * @param  {String} 样式内容
     * @return {Void}
     */
    _p.__injectCSSText = function(_style,_css){
        _style.textContent = _css;
    };
    /**
     * 对样式进行预处理
     * @param  {String} 待处理样式内容
     * @return {String} 处理后样式内容
     */
    _p.__processCSSText = (function(){
        var _reg0 = /\$<(.*?)>/gi,
            _reg1 = /\{(.*?)\}/g,
            _pfx = '-'+_opfx.css.toLowerCase()+'-',
            _2dmap = {
                scale:'scale({x|1},{y|1})',
                rotate:'rotate({a})',
                translate:'translate({x},{y})',
                matrix:'matrix({m11},{m12},{m21},{m22},{m41},{m42})'
            },
            _3dmap  = {
                scale:'scale3d({x|1},{y|1},{z|1})',
                rotate:'rotate3d({x},{y},{z},{a})',
                translate:'translate3d({x},{y},{z})',
                matrix:'matrix3d({m11},{m12},{m13},{m14},{m21},{m22},{m23},{m24},{m31},{m32},{m33|1},{m34},{m41},{m42},{m43},{m44|1})'
            };
// merge template and data
        var _getTransformValue = function(_tpl,_map){
            _map = _map||_o;
            return _tpl.replace(_reg1,function($1,$2){
                var _arr = $2.split('|');
                return _map[_arr[0]]||_arr[1]||'0';
            });
        };
// process transform value
        _p.__processTransformValue = function(_name,_data){
            var _tpl = (!_ospt.css3d?_2dmap:_3dmap)[_name.trim()];
            if (!!_tpl){
                return _getTransformValue(_tpl,_data);
            }
            return '';
        };
        return function(_css){
            if (!_css.replace){
                return _css;
            }
            return _css.replace(_reg0,function($1,$2){
// prefix for css3
                if ($2==='vendor'){
                    return _pfx;
                }
// parse 3D value
                var _arr = ($2||'').split('|');
                return _p.__processTransformValue(
                        _arr[0],_u._$query2object(_arr[1])
                    )||$1;
            });
        };
    })();
    /**
     * 追加CSS规则
     * @param  {Node}    样式节点
     * @param  {String}  单条样式规则
     * @return {CSSRule} 样式规则对象
     */
    _p.__appendCSSText = function(_element,_css){
        var _sheet = _element.sheet,
            _length = _sheet.cssRules.length;
        _sheet.insertRule(_css,_length);
        return _sheet.cssRules[_length];
    };
    /**
     * 取待验证的样式列表
     * @param  {String} 样式，多个以空格分隔
     * @return {Array}  样式列表
     */
    _p.__getClassList = (function(){
        var _reg = /\s+/;
        return function(_class){
            _class = (_class||'').trim();
            return !!_class?_class.split(_reg):null;
        };
    })();
    /**
     * 操作样式
     * @param  {Node}   节点
     * @param  {String} 操作
     * @param  {String} 样式
     * @return {Void}
     */
    _p.__processClassName = function(_element,_type,_class){
        if (_type=='replace'){
            _p.__processClassName(
                _element,'remove',_class
            );
            _p.__processClassName(
                _element,'add',arguments[3]
            );
            return;
        }
        _u._$forEach(
            _p.__getClassList(_class),
            function(_clazz){
                _element.classList[_type](_clazz);
            }
        );
    };
    /**
     * 检测节点是否包含指定样式，多个样式用空格分隔，检测时包含其中之一即表示包含
     * @param  {Node}    节点ID或者对象
     * @param  {String}  样式串
     * @return {Boolean} 是否含指定样式
     */
    _p.__hasClassName = function(_element,_class){
        var _list = _element.classList;
        if (!_list||!_list.length){
            return !1;
        }
        return _u._$indexOf(
                _p.__getClassList(_class),
                function(_clazz){
                    return _list.contains(_clazz);
                }
            )>=0;
    };
// for init
    (function(){
        if (!_ospt.css3d){
            var _matrix = _p.__getCSSMatrix();
            _ospt.css3d = !!_matrix&&_matrix.m41!=null;
        }
    })();
    return _p;
},2,17);
I$(21,function(_h,_m,_u,_p,_o,_f,_r){var _k_ = (CMPT?NEJ.P("nej.p"):arguments[1])._$KERNEL;if (_k_.engine=='trident'){(function (){
    /**
     * 取节点的子节点列表
     * @param  {Node} _element 节点ID或者对象
     * @return {Array}         子节点列表
     */
    _h.__getChildren = _h.__getChildren._$aop(
        function(_event){
            var _element = _event.args[0];
            if (!!_element.children) return;
// hack children
            _event.stopped = !0;
            var _result = [];
            _u._$forEach(
                _element.childNodes,
                function(_node){
                    if (_node.nodeType==1){
                        _result.push(_node);
                    }
                }
            );
            _event.value = _result;
        }
    );
})();}
    if (_k_.engine=='trident'&&_k_.release<='6.0'){(function (){
        /**
         * 设置、获取数据
         * @param {Node}     节点
         * @param {String}   标识
         * @param {Variable} 值
         */
        _h.__dataset = (function(){
            var _dataset = {},
                _tag = 'data-',
                _reg = /\-(.{1})/gi;
// init element dataset
            var _init = function(_element){
                var _id = _element.id;
                if (!!_dataset[_id]) return;
                var _map = {};
                _u._$forEach(
                    _element.attributes,
                    function(_node){
                        var _key  = _node.nodeName;
                        if (_key.indexOf(_tag)!=0) return;
                        _key = _key.replace(_tag,'')
                            .replace(_reg,function($1,$2){
                                return $2.toUpperCase();
                            });
                        _map[_key] = _node.nodeValue||'';
                    }
                );
                _dataset[_id] = _map;
            };
            return function(_element,_key,_value){
                _init(_element);
                var _set = _dataset[_element.id];
                if (_value!==undefined){
                    _set[_key] = _value;
                }
                return _set[_key];
            };
        })();
    })();}
    if (_k_.engine=='trident'&&_k_.release<='5.0'){(function (){
// cache background image
        try{document.execCommand('BackgroundImageCache',!1,!0);}catch(e){}
        /**
         * 注入样式
         * @param  {Node}   样式节点
         * @param  {String} 样式内容
         * @return {Void}
         */
        _h.__injectCSSText = (function(){
            var _max = 30;
            return _h.__injectCSSText._$aop(function(_event){
                var _element = _event.args[0];
                if (!_element.styleSheet) return;
                _event.stopped = !0;
                var _css = _event.args[1];
// ie9- has 31 style/link limitation
                var _list = document.styleSheets;
                if (_list.length>_max){
// bad performance
                    _element = _list[_max];
                    _css = _element.cssText + _css;
                }else{
                    _element = _element.styleSheet;
                }
                _element.cssText = _css;
            });
        })();
        /**
         * 取待验证的样式正则表达式
         * @param  {String} 样式，多个以空格分隔
         * @return {RegExp} 正则表达式
         */
        _h.__getClassRegExp = (function(){
            var _reg = /\s+/g;
            return function(_class){
                _class = (_class||'').trim().replace(_reg,'|');
                return !_class?null:new RegExp('(\\s|^)(?:'+_class+')(?=\\s|$)','g');
            };
        })();
        /**
         * 操作样式
         * @param  {Node}   节点
         * @param  {String} 操作
         * @param  {String} 样式
         * @return {Void}
         */
        _h.__processClassName = function(_element,_type,_class){
            _class = _class||'';
            var _name = _element.className||'',
                _xreg = _h.__getClassRegExp(
                    _class+' '+(arguments[3]||'')
                );
// remove all calss
            var _result = _name;
            if (!!_xreg){
                _result = _result.replace(_xreg,'');
            }
// parse added class
            switch(_type){
                case 'remove':
                    _class = '';
                    break;
                case 'replace':
                    _class = arguments[3]||'';
                    break;
            }
// generate class result
            _result = (_result+' '+_class).trim();
            if (_name!=_result){
                _element.className = _result;
            }
        };
        /**
         * 检测节点是否包含指定样式，多个样式用空格分隔，检测时包含其中之一即表示包含
         * @param  {Node}    节点ID或者对象
         * @param  {String}  样式串
         * @return {Boolean} 是否含指定样式
         */
        _h.__hasClassName = function(_element,_class){
            var _xreg = _h.__getClassRegExp(_class);
            if (!!_xreg){
                return _xreg.test(_element.className||'');
            }
            return !1;
        };
    })();}
    if (_k_.engine=='trident'&&_k_.release<='4.0'){(function (){
        /**
         * 根据类名取节点列表
         * @param  {Node}   节点ID或者对象
         * @param  {String} 类名
         * @return {Array}  节点列表
         */
        _h.__getElementsByClassName = function(_element,_class){
            var _result = [],
                _regexp = new RegExp('(\\s|^)(?:'+_class.replace(/\s+/g,'|')+')(?=\\s|$)');
            _u._$forEach(
                _element.getElementsByTagName('*'),
                function(_node){
                    if (_regexp.test(_node.className)){
                        _result.push(_node);
                    }
                }
            );
            return _result;
        };
        /**
         * 取下一个兄弟节点
         * @param  {Node}  节点对象
         * @return {Node}  节点
         */
        _h.__nextSibling = function(_element){
            while(_element=_element.nextSibling){
                if (_element.nodeType==1){
                    return _element;
                }
            }
        };
        /**
         * 取上一个兄弟节点
         * @param  {Node}  节点对象
         * @return {Node}  节点
         */
        _h.__previousSibling = function(_element){
            while(_element=_element.previousSibling){
                if (_element.nodeType==1){
                    return _element;
                }
            }
        };


        /**
         * 取样式值
         * @param  {String|Node} 节点
         * @param  {String}      样式名称
         * @return {Variable}    样式值
         */
        _h.__getStyleValue = (function(){
            var _reg0 = /opacity\s*=\s*([\d]+)/i;
            var _fmap = {
// get opacity from filter:alpha(opacity=50)
                opacity:function(_style){
                    var _result = 0;
                    if (_reg0.test(_style.filter||'')){
                        _result = parseFloat(RegExp.$1)/100;
                    }
                    return _result;
                }
            };
            return function(_element,_name){
                var _current = _element.currentStyle,
                    _func = _fmap[_name];
                if (!!_func){
                    return _func(_current);
                }
                return _current[_h.__getStyleName(_name)]||'';
            };
        })();
        /**
         * 设置样式
         * @param  {String|Node} 节点
         * @param  {String}      样式名称
         * @param  {String}      样式值
         * @return {Void}
         */
        _h.__setStyleValue = (function(){
            var _fmap = {
// opacity -> filter:alpha(opacity=50)
                opacity:function(_element,_value){
                    _element.style.filter = 'alpha(opacity='+_value*100+')';
                }
            };
            return function(_element,_name,_value){
                var _func = _fmap[_name];
                if (!!_func){
                    _func(_element,_value);
                }else{
                    _element.style[_h.__getStyleName(_name)] = _value;
                }
            };
        })();
        /**
         * 追加CSS规则
         * @param  {Node}    样式节点
         * @param  {String}  单条样式规则
         * @return {CSSRule} 样式规则对象
         */
        _h.__appendCSSText = function(_element,_css){
            var _sheet = _element.styleSheet,
                _length = _sheet.rules.length,
                _arr = _css.split(/[\{\}]/);
            _sheet.addRule(_arr[0],_arr[1],_length);
            return _sheet.rules[_length];
        };
    })();}
    if (_k_.engine=='trident'&&_k_.release<='3.0'){(function (){
        /**
         * 取节点属性值
         * @param  {Node}   节点
         * @param  {String} 属性名
         * @return {String} 属性值
         */
        _h.__getAttribute =
            _h.__getAttribute._$aop(null,function(_event){
// fix ie7 maxlength default value 2147483647
                var _args = _event.args;
                if (_args[1]=='maxlength'&&
                    _event.value==2147483647){
                    _event.value = null;
                }
            });
    })();}
    if (_k_.engine=='trident'&&_k_.release<='2.0'){(function (){
        /**
         * 节点占全屏
         * @param  {Node}   节点
         * @param  {Object} 视窗模型
         * @return {Void}
         */
        _h.__fullScreen = function(_element,_viewport){
            var _style = _element.style;
            _style.width = _viewport.scrollWidth+'px';
            _style.height = _viewport.scrollHeight+'px';
        };
        /**
         * 为节点增加用于盖select/flash等控件的层
         * @param  {Node} 节点
         * @return {Void}
         */
        _h.__mask = (function(){
            var _cache = {};
// remove mask
            _h.__unmask = function(_element){
                var _id = _element.id,
                    _mask = _cache[_id];
                if (!!_mask){
                    delete _cache[_id];
                    _mask.parentNode.removeChild(_mask);
                }
            };
// append mask
            return function(_element){
                var _id = _element.id,
                    _mask = _cache[_id];
// create mask
                if (!_mask){
                    _mask = document.createElement('iframe');
                    _mask.style.position = 'absolute';
                    _cache[_id] = _mask;
                }
// sync mask size
                var _style1 = _mask.style,
                    _style0 = _element.style;
                _style1.top = (parseInt(_style0.top)||0)+'px';
                _style1.left = (parseInt(_style0.left)||0)+'px';
                _style1.width = _element.offsetWidth+'px';
                _style1.height = _element.offsetHeight+'px';
                _element.insertAdjacentElement('beforeBegin',_mask);
                return _mask;
            };
        })();
    })();}
    if (_k_.engine=='gecko'){(function (){
        if (!_m._$SUPPORT.css3d){
            _m._$SUPPORT.css3d = 'MozPerspective' in document.body.style;
        }
        if (!('insertAdjacentElement' in document.body)){
            HTMLElement.prototype.insertAdjacentElement = function(_where,_element){
                if (!_where||!_element) return;
                switch(_where){
                    case 'beforeEnd'  :
                        this.appendChild(_element);
                        return;
                    case 'beforeBegin':
                        this.parentNode.insertBefore(_element,this);
                        return;
                    case 'afterBegin' :
                        !this.firstChild
                            ?this.appendChild(_element)
                            :this.insertBefore(_element,this.firstChild);
                        return;
                    case 'afterEnd'   :
                        !this.nextSibling
                            ?this.parentNode.appendChild(_element)
                            :this.parentNode.insertBefore(_element,this.nextSibling);
                        return;
                }
            };
        }
        if (!('innerText' in document.body)){
            HTMLElement.prototype['__defineGetter__']("innerText",function(){return this.textContent;});
            HTMLElement.prototype['__defineSetter__']("innerText",function(_content){this.textContent = _content;});
        }
    })();};return _h;
},25,17,2);
I$(4,function (NEJ,_g,_u,_v,_x,_h,_p,_o,_f,_r){
// variables
    var _y = {},     // chainable methods
        _cspol,      // css text pool
        _empol = {}, // elements without id property, eg. document,window
        _dirty = {}, // temporary element with id
        _fragment = document.createDocumentFragment(); // node in memory
// init
    if (!document.head){
        document.head = document.getElementsByTagName('head')[0]||document.body;
    }
    /**
     * 为节点设置一个唯一的标识
     *
     * 结构举例
     * ```html
     *    <div id="abc">aaaaa</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 如果有id，返回原来的id,否则返回auto-id-12345678(8位随机字符串)
*       var _id = _e._$id(_node||"abc");
*   });
     * ```
     *
     * @method module:base/element._$id
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @return {String}             节点标识
     */
    /**
     * @method CHAINABLE._$id
     * @see module:base/element._$id
     */
    _p._$id =
        _y._$id = function(_element){
            _element = _p._$get(_element);
            if (!_element) return;
            var _id = !!_element.id ? _element.id
                : 'auto-id-'+_u._$uniqueID();
            if (!('id' in _element)){
                _empol[_id] = _element;
            }
            _element.id = _id;
// check if element can be getted
            if (!_p._$get(_id)){
                _dirty[_id] = _element;
            }
            return _id;
        };
    /**
     * 根据标识取节点对象，包括在内存中的节点
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 先根据id从内存中取，再从页面取
*       var _node = _e._$get("abc");
*   });
     * ```
     *
     * @method module:base/element._$get
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @return {Node}               节点对象
     */
    _p._$get = function(_element){
// for document/window
        var _node = _empol[''+_element];
        if (!!_node){
            return _node;
        }
// element is node
        if (!_u._$isString(_element)&&
            !_u._$isNumber(_element)){
            return _element;
        }
// element is id
// check node in page first
        var _node = document.getElementById(_element);
        if (!_node){
            _node = _h.__getElementById(_fragment,_element);
        }
// remove dirty element
        if (!!_node){
            delete _dirty[_element];
        }
        return _node||_dirty[_element];
    };
    /**
     * 取节点的子节点列表
     *
     * 结构举例
     * ```html
     *   <div id="abc">
     *       <p>1</p>
     *       <p><span>2</span></p>
     *       <p>3</p>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 取直接的3个子节点(p标签)
*       var _childs = _e._$getChildren('abc');
*
*       // 使用类名过滤，去带a或者b样式类的子节点
*       var _childs = _e._$getChildren('abc','a b');
*   });
     * ```
     *
     * @method module:base/element._$getChildren
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @param  {String}      arg1 - 样式标识
     * @return {Array}              子节点列表
     */
    /**
     * @method CHAINABLE._$getChildren
     * @see module:base/element._$getChildren
     */
    _p._$getChildren =
        _y._$getChildren = function(_element,_clazz){
            _element = _p._$get(_element);
            if (!_element) return null;
            var _list = _h.__getChildren(_element);
            if (!!_clazz){
                _u._$reverseEach(
                    _list,function(_node,_index,_list){
                        if (!_p._$hasClassName(_node,_clazz)){
                            _list.splice(_index,1);
                        }
                    }
                );
            }
            return _list;
        };
    /**
     * 根据类名取节点列表
     *
     * 结构举例
     * ```html
     *   <div id="abc">
     *     <p class="item">1</p>
     *     <div><p class="item">2</p></div>
     *     <p class="item">3</p>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 获取abc节点下样式带有"item"的节点列表,如果没有父节点，返回null
*       var _list = _e._$getByClassName('abc','item');
*   });
     * ```
     *
     * @method module:base/element._$getByClassName
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @param  {String}      arg1 - 类名
     * @return {Array}              节点列表
     */
    /**
     * @method CHAINABLE._$getByClassName
     * @see module:base/element._$getByClassName
     */
    _p._$getByClassName =
        _y._$getByClassName = function(_element,_class){
            _element = _p._$get(_element);
            return !_element ? null :
                _h.__getElementsByClassName(
                    _element,_class.trim()
                );
        };
    /**
     * 根据从兄弟节点中搜索符合条件的节点
     *
     * 结构举例
     * ```html
     *   <div>
     *     <p class="item" id="a1">1</p>
     *     <p class="item" id="a2">2</p>
     *     <p class="item" id="a3">3</p>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 取a2的后一个兄弟节点a3
*       var _node = _e._$getSibling('a2');
*
*       // 取a2的前一个兄弟节点a1
*       var _node = _e._$getSibling('a2',{backward:true});
*
*       // 过滤搜索，从a2向后搜索找id为a4的节点
*       var _node = _e._$getSibling('a2',function(_element){
*           return _element.id=='a4'
*       });
*
*       // 过滤搜索，从a2向前搜索找id为a0的节点
*       var _node = _e._$getSibling('a2',{
*           backward:true,
*           filter:function(_element){
*               return _element.id=='a0'
*           }
*       });
*   });
     * ```
     *
     * @method   module:base/element._$getSibling
     * @param    {String|Node}     arg0     - 节点标识或者对象
     * @param    {Function|Object} arg1     - 如果是函数则表示过滤器，否则为配置信息
     * @property {Boolean}         backward - 是否后向搜索，默认前向搜索
     * @property {Function}        filter   - 节点过滤器，返回true表示需要返回的节点，找到第一个即返回
     * @return   {Node}                       符合条件的节点
     */
    /**
     * @method CHAINABLE._$getSibling
     * @see module:base/element._$getSibling
     */
    _p._$getSibling =
        _y._$getSibling = (function(){
            var _doFilter = function(){
                return !0;
            };
            return function(_element,_filter){
                _element = _p._$get(_element);
                if (!_element){
                    return null;
                }
                var _conf = {
                    backward:!1,
                    filter:_doFilter
                };
                if (_u._$isFunction(_filter)){
                    _conf.filter = _filter;
                }else{
                    _conf = _u._$fetch(_conf,_filter);
                }
                var _next = _conf.backward
                    ? _h.__previousSibling
                    : _h.__nextSibling;
                while(_element=_next(_element)){
                    if (_conf.filter(_element)){
                        break;
                    }
                }
                return _element;
            };
        })();
    /**
     * 取节点所在的滚动容器，
     * 从当前节点开始往上遍历，直到出现滚动条的节点
     *
     * 结构举例
     * ```html
     *   <div id="efg">
     *     <div id="abc">123</div>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 加入efg节点出现滚动条，则这里找到的是efg节点
*       var _sbody = _e._$getScrollViewPort('abc');
*
*       // 不带任何参数取页面滚动条所在节点
*       var _sbody = _e._$getScrollViewPort();
*   });
     * ```
     *
     * @method module:base/element._$getScrollViewPort
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @return {Node}               视窗节点
     */

    /**
     * 盒模型结构
     *
     * @typedef  {Object} module:base/element~BoxModel
     * @property {Number} scrollTop    - 滚动垂直偏移
     * @property {Number} scrollLeft   - 滚动水平偏移
     * @property {Number} clientWidth  - 页面可视宽度
     * @property {Number} clientHeight - 页面可视高度
     * @property {Number} scrollWidth  - 页面滚动宽度
     * @property {Number} scrollHeight - 页面滚动高度
     */
    /**
     * 取页面盒信息，返回盒信息内容：
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 返回信息见说明
*       var _box = _e._$getPageBox();
*   });
     * ```
     *
     * @method module:base/element._$getPageBox
     * @param  {Document} arg0 - 文档对象
     * @return {module:base/element~BoxModel} 盒信息
     */

    /**
     * 按比例将给定大小缩放至限制区域内
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 限制区域大小 100*10
*       var _limit = {width:100,height:10};
*
*       // 给定200*10的大小，由于宽度超出，缩放后为{width:100,height:5}
*       var _box = _e._$getMaxBox({width:200,height:10},_limit);
*
*       // 给定100*20的大小，由于高度超出，缩放后为{width:50,height:10}
*       var _box = _e._$getMaxBox({width:100,height:20},_limit);
*
*       // 给定 50*5，没有超出限制，返回{width:50,height:5}
*       var _box = _e._$getMaxBox({width:50,height:5},_limit);
*   });
     * ```

    /**
     * 滚动到指定节点
     *
     * 结构举例
     * ```html
     *   <div id="a" style="padding:5px 0 0 10px;"></div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 滚动到页面上a这节点的位置
*       _e._$scrollTo('a');
*   });
     * ```
     *
     * @method module:base/element._$scrollTo
     * @param  {Node|String} arg0 - 节点
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$scrollTo
     * @see module:base/element._$scrollTo
     */

    /**
     * 大小信息对象
     * @typedef  {Object} module:base/element~SizeModel
     * @property {Number} width  - 宽度
     * @property {Number} height - 高度
     */
    /**
     * 位置信息对象
     * @typedef  {Object} module:base/element~PositionModel
     * @property {Number} top  - 垂直位置
     * @property {Number} left - 水平位置
     */
    /**
     * 计算在容器中对齐时的位置信息
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 容器大小
*       var _box = {width:100,height:40};
*
*       // 默认居中对齐返回 {top:15,left:40}
*       var _pos = _e._$align(_box,{width:20,height:10});
*
*       // 左下对齐返回 {top:30,left:0}
*       var _pos = _e._$align(_box,{width:20,height:10},'left bottom');
*   });
     * ```
     *
     * @method module:base/element._$align
     * @param  {module:base/element~SizeModel} arg0 - 容器大小
     * @param  {module:base/element~SizeModel} arg1 - 原始大小
     * @param  {String} arg2 - 对齐方式，水平+空格+垂直，如left top，默认为 center middle，
     *                         水平：left/center/right，
     *                         垂直：top/middle/bottom
     * @return {module:base/element~PositionModel} 位置信息
     */
    _p._$align = (function(){
        var _reg = /\s+/;
        var _fmap = {
            left:function(){
                return 0;
            },
            center:function(_box,_org){
                return (_box.width-_org.width)/2;
            },
            right:function(_box,_org){
                return _box.width-_org.width;
            },
            top:function(){
                return 0;
            },
            middle:function(_box,_org){
                return (_box.height-_org.height)/2;
            },
            bottom:function(_box,_org){
                return _box.height-_org.height;
            }
        };
        return function(_box,_org,_align){
            var _result = {},
                _arr  = (_align||'').split(_reg),
                _top  = _fmap[_arr[1]]||_fmap.middle,
                _left = _fmap[_arr[0]]||_fmap.center;
            _result.top = _top(_box,_org);
            _result.left = _left(_box,_org);
            return _result;
        };
    })();
    /**
     * 计算两个节点之间的偏移量
     *
     * 结构举��
     * ```html
     *   <div id="a" style="position:relative;padding:5px 0 0 10px;">
     *     <span id="b">123</span>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 计算节点b到节点a(外层需要定位属性)的距离，如果没有指定节点，默认计算的根节点
*       // _result : {x:10,y:5}
*       var _result = _e._$offset('b','a');
*   });
     * ```
     *
     * @method module:base/element._$offset
     * @param  {String|Node} arg0 - 起始节点
     * @param  {String|Node} arg1 - 结束节点，没有该参数则计算到根节点
     * @return {Object}             偏移量，如{x:234,y:987}
     */
    /**
     * @method CHAINABLE._$offset
     * @see module:base/element._$offset
     */
    _p._$offset =
        _y._$offset = (function(){
            var _isRoot = function(_element){
                return _element==document.body||
                    _element==document.documentElement;
            };
            return function(_from,_to){
                _from = _p._$get(_from);
                if (!_from){
                    return null;
                }
                _to = _p._$get(_to)||null;
                var _node = _from,
                    _result = {x:0,y:0},
                    _isroot,_delta,_border;
                while(!!_node&&_node!=_to){
                    _isroot = _isRoot(_node)||_node==_from;
                    _delta = _isroot?0:_node.scrollLeft;
                    _border = parseInt(_p._$getStyle(_node,'borderLeftWidth'))||0;
                    _result.x += _node.offsetLeft+_border-_delta;
                    _delta = _isroot?0:_node.scrollTop;
                    _border = parseInt(_p._$getStyle(_node,'borderTopWidth'))||0;
                    _result.y += _node.offsetTop+_border-_delta;
                    _node = _node.offsetParent;
                }
                return _result;
            };
        })();
    /**
     * 节点占全屏
     *
     * @method module:base/element._$fullScreen
     * @param  {Node} arg0 - 节点
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$fullScreen
     * @see module:base/element._$fullScreen
     */
    _p._$fullScreen =
        _y._$fullScreen = function(_element){
            _element = _p._$get(_element);
            if (!!_element){
                _h.__fullScreen(
                    _element,
                    _p._$getPageBox()
                );
            }
        };
    /**
     * 为节点增加用于盖select/flash等控件的层
     *
     * @method module:base/element._$mask
     * @see    module:base/element._$unmask
     * @param  {Node} arg0 - 节点
     * @return {Node}        盖层节点
     */
    /**
     * @method CHAINABLE._$mask
     * @see module:base/element._$mask
     */

    /**
     * 为节点移除用于盖select/flash等控件的层
     *
     * @method module:base/element._$unmask
     * @see    module:base/element._$mask
     * @param  {Node} arg0 - 节点
     * @return {Node}        盖层节点
     */
    /**
     * @method CHAINABLE._$unmask
     * @see module:base/element._$unmask
     */
    _p._$unmask =
        _y._$unmask = function(_element){
            _element = _p._$get(_element);
            if (!!_element){
                _p._$id(_element);
                return _h.__unmask(_element);
            }
            return null;
        };
    /**
     * 创建节点，使用该接口创建的结构后续可通过_$get接口根据ID取到节点
     *
     * 结构举例
     * ```javascript
     *   <div id="abc">1</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 创建一个节点，挂到body上
*       _e._$create("div","m-body",document.body);
*
*       // 创建一个节点挂到id是abc的节点上
*       // 结果：<div id="abc">1<p class="m-list"></p></div>
*       _e._$create("p","m-list","abc");
*
*       // 创建一个节点放在内存中
*       var _node = _e._$create('div');
*       _node.innerHTML = '<p id="a">aaaaaa</p><p id="b">bbbbbb</p>';
*       // 后续可以通过id取id为a的节点
*       var _pa = _e._$get('a');
*   });
     * ```
     *
     * @method module:base/element._$create
     * @param  {String}      arg0 - 标签
     * @param  {String}      arg1 - 样式
     * @param  {String|Node} arg2 - 父节点标识或者对象
     * @return {Node}               节点
     */
    _p._$create = (function(){
        var _map = {
            a:{href:'#',hideFocus:!0},
            style:{type:'text/css'},
            link:{type:'text/css',rel:'stylesheet'},
            iframe:{frameBorder:0},
            script:{defer:!0,type:'text/javascript'}
        };
        return function(_tag,_class,_parent){
            var _element = document.createElement(_tag),
                _config = _map[_tag.toLowerCase()];
            _u._$merge(_element,_config);
            if (!!_class) _element.className = _class;
            _parent = _p._$get(_parent);
            if (!!_parent){
                _parent.appendChild(_element);
            }else{
// append to documentfragment for get by id
                if (!_config){
                    _fragment.appendChild(_element);
                }
            }
            return _element;
        };
    })();
    /**
     * 创建可交互框架
     *
     * 结构举例
     * ```html
     *   <div id="frameCnt"></div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*      var _xFrame = _e._$createXFrame({
*          src:'http://www.baidu.com',
*          name:'百度',
*          parent:'frameCnt',
*          visible:false,
*          onload:function(){
*              // 加载frame成功后，name设置成功，为百度
*              // 加载frame成功后，显示效果正确，display:none
*          }
*      });
*   });
     * ```
     *
     * @method   module:base/element._$createXFrame
     * @param    {Object}               arg0    - 可选配置参数
     * @property {String}               src     - 框架地址
     * @property {String}               name    - 框架名称
     * @property {String|Node|Function} parent  - 父节点或者框架加入父容器的执行函数
     * @property {Boolean}              visible - 是否可见
     * @property {Function}             onload  - 框架载入回调
     * @return {Node}                             框架节点
     */
    _p._$createXFrame = (function(){
        var _getFrameSrc = function(){
            if (location.hostname==document.domain){
                return 'about:blank';
            }
            return 'javascript:(function(){document.open();document.domain="'+document.domain+'";document.close();})();';
        };
        var _getFrameWithName = function(_name){
            _name = _name.trim();
            if (!_name){
                return _p._$create('iframe');
            }
// pass name to frame
            var _iframe;
            try{
                _iframe = document.createElement(
                    '<iframe name="'+_name+'"></iframe>');
                _iframe.frameBorder = 0;
            }catch(e){
                _iframe = _p._$create('iframe');
                _iframe.name = _name;
            }
            return _iframe;
        };
        return function(_options){
            _options = _options||_o;
            var _iframe = _getFrameWithName(_options.name||'');
            if (!_options.visible){
                _iframe.style.display = 'none';
            }
            if (_u._$isFunction(_options.onload)){
                _v._$addEvent(_iframe,'load',function(_event){
                    if (!_iframe.src) return;
                    _v._$clearEvent(_iframe,'load');
                    _options.onload(_event);
                });
            }
// will trigger onload
            var _parent = _options.parent;
            if (_u._$isFunction(_parent)){
                try{_parent(_iframe);}catch(e){}
            }else{
                (_p._$get(_parent)||document.body).appendChild(_iframe);
            }
// ensure trigger onload async
            var _src = _options.src||_getFrameSrc();
            window.setTimeout(function(){
                _iframe.src = _src;
            },0);
            return _iframe;
        };
    })();
    /**
     * 删除节点
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 移除节点前先清理节点上的事件
*       _e._$remove('abc',false);
*       // 移除节点前不清理节点上的事件
*       _e._$remove('abc',true);
*   });
     * ```
     *
     * @method module:base/element._$remove
     * @see    module:base/element._$removeByEC
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @param  {Boolean}     arg1 - 是否禁止事件清理
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$remove
     * @see module:base/element._$remove
     */
    _p._$remove =
        _y._$remove = (function(){
            var _fmap = {
                img:function(_node){
                    _node.src = _g._$BLANK_IMAGE;
                },
                iframe:function(_node){
                    _node.src = 'about:blank';
                }
            };
            var _doClear = function(_node,_tag){
                if (!_tag){
                    var _xtag = (_node.tagName||'').toLowerCase(),
                        _func = _fmap[_xtag];
                    if (!!_func){
                        _func(_node);
                    }
                    return;
                }
                if (!!_node.getElementsByTagName){
                    _u._$forEach(
                        _node.getElementsByTagName(_tag),
                        _doClear
                    );
                }
            };
            return function(_element){
                _element = _p._$get(_element);
                if (!!_element){
// clear events
                    if (!arguments[1]){
                        _v._$clearEvent(_element);
                    }
// clear elements
                    _doClear(_element);
                    _doClear(_element,'img');
                    _doClear(_element,'iframe');
// remove node
                    if (!!_element.parentNode){
                        _element.parentNode.removeChild(_element);
                    }
                }
            };
        })();
    /**
     * 节点移至内存
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 先生成一个节点加到body下
*       var _node = _e._$create('div','js-div',document.body);
*       // 把节点移动到内存中
*       _e._$removeByEC(_node);
*       // 从body上没有取到节点,结果为[]
*       _e._$getByClassName(document.body,'js-div');
*   });
     * ```
     *
     * @method module:base/element._$removeByEC
     * @see    module:base/element._$remove
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$removeByEC
     * @see module:base/element._$removeByEC
     */
    _p._$removeByEC =
        _y._$removeByEC = function(_element){
            _element = _p._$get(_element);
            if (!!_element){
                try{
                    _fragment.appendChild(_element);
                }catch(ex){
// ignore
                    console.error(ex);
                }
            }
        };
    /**
     * 清除所有子节点
     *
     * 结构举例
     * ```html
     *   <ul id="abc">
     *     <li>aaaaaaaaaaaaa</li>
     *     <li>bbbbbbbbbbbbb</li>
     *     <li>ccccccccccccc</li>
     *   </ul>
     *
     *   <table id="efg">
     *     <tr><td>1111</td><td>1111</td></tr>
     *     <tr><td>2222</td><td>2222</td></tr>
     *     <tr><td>3333</td><td>3333</td></tr>
     *   </table>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 清除ul下的子节点
*       _e._$clearChildren('abc');
*
*       // 清除table下的子节点
*       _e._$clearChildren('efg');
*   });
     * ```
     *
     * @method module:base/element._$clearChildren
     * @see    module:base/element._$remove
     * @param  {String|Node} arg0 - 容器节点
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$clearChildren
     * @see module:base/element._$clearChildren
     */
    _p._$clearChildren =
        _y._$clearChildren = function(_element){
            _element = _p._$get(_element);
            if (!!_element){
                _u._$reverseEach(
                    _element.childNodes,
                    function(_node){
                        _p._$remove(_node);
                    }
                );
            }
        };
    /**
     * 内联元素增加定位封装
     *
     * 结构举例
     * ```html
     *   <input type="text" id="abc"/>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 包装定位的span
*       _e._$wrapInline('abc');
*   });
     * ```
     *
     * 生成结构如下
     * ```html
     *   <span style="position:relative;zoom:1">
     *     <input type="text" id="abc"/>
     *     <!-- 此api返回以下这个节点 -->
     *     <span style="position:absolute;top:0;left:0;"></span>
     *   </span>
     * ```
     *
     * 应用举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 返回容器的样式名称
*       // 通过这个样式名称可以取到一个绝对定位的样式名 class+'-show'
*       var _node = _e._$wrapInline('abc',{
*           tag:'label',
*           clazz:'js-xxx'
*       });
*       // 可以在返回的节点里添加想要显示的结构
*       _node.innerHTML = '<span>aaa</span><span>aaa</span>';
*   });
     * ```
     *
     * @method   module:base/element._$wrapInline
     * @param    {String|Node}  arg0  - 内联节点
     * @param    {Object}       arg1  - 绝对定位节点配置信息
     * @property {String}       tag   - 标记名称，默认span
     * @property {String}       nid   - 节点识别样式名，这个会被添加到样式中作为标识
     * @property {String}       clazz - 样式名称
     * @return   {Node}                 绝对定位的节点
     */
    /**
     * @method CHAINABLE._$wrapInline
     * @see module:base/element._$wrapInline
     */
    _p._$wrapInline =
        _y._$wrapInline = (function(){
            var _clazz,
                _reg0 = /\s+/;
            var _doInitStyle = function(){
                if (!!_clazz) return;
                _clazz = _p._$pushCSSText('.#<uispace>{position:relative;zoom:1;}.#<uispace>-show{position:absolute;top:0;left:100%;cursor:text;white-space:nowrap;overflow:hidden;}');
                _p._$dumpCSSText();
            };
            return function(_element,_options){
                _element = _p._$get(_element);
                if (!_element){
                    return null;
                }
// init style
                _doInitStyle();
                _options = _options||_o;
// check relative parent
                var _parent = _element.parentNode;
                if (!_p._$hasClassName(_parent,_clazz)){
// build wrapper box
                    _parent = _p._$create('span',_clazz);
                    _element.insertAdjacentElement('beforeBegin',_parent);
                    _parent.appendChild(_element);
                }
// check absolute node
                var _nid = _options.nid||'',
                    _node = _p._$getByClassName(
                        _parent,_nid||
                        (_clazz+'-show')
                    )[0];
                if (!_node){
                    var _klass = ((_options.clazz||'')+' '+_nid).trim();
                    _klass = _clazz+'-show'+(!_klass?'':' ')+_klass;
                    _node = _p._$create(_options.tag||'span',_klass);
                    _parent.appendChild(_node);
                }
// append class to parent node
                var _klass = _options.clazz;
                if (!!_klass){
                    _klass = (_klass||'').trim().split(_reg0)[0]+'-parent';
                    _p._$addClassName(_parent,_klass);
                }
                return _node;
            };
        })();
    /**
     * 设置或者获取指定标识的数据
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 设置值操作
*       // <div id="abc" data-img="http://a.b.com/a.png">123</div>
*       // 返回value值: http://a.b.com/a.png
*       var _src = _e._$dataset('abc','img','http://a.b.com/a.png');
*       // 取值操作
*       var _src = _e._$dataset('abc','img');
*
*       // 批量设置
*       var _map = _e._$dataset('abc',{
*           a:'aaaaa',
*           b:'bbbbbbbb',
*           c:'ccccccccc'
*       });
*
*       // 批量取值
*       // 返回：{a:'aaaaa',b:'bbbbbbbb',c:'ccccccccc'}
*       var _map = _e._$dataset('abc',['a','b','c']);
*   });
     * ```
     *
     * @method module:base/element._$dataset
     * @see    module:base/element._$attr
     * @param  {String}              arg0 - 数据标识
     * @param  {String|Object|Array} arg1 - 属性名
     * @return {String|Object}              数据值
     */
    /**
     * @method CHAINABLE._$dataset
     * @see module:base/element._$dataset
     */
    _p._$dataset =
        _y._$dataset = function(_element,_key,_value){
// check element
            var _id = _p._$id(_element);
            if (!_id){
                return null;
            }
// check single key-value
            if (_u._$isString(_key)){
                return _h.__dataset(
                    _p._$get(_element),
                    _key,_value
                );
            }
// check map set
// ignore argument _value
            if (_u._$isObject(_key)){
                var _ret = {};
                _u._$forIn(_key,function(_v,_k){
                    _ret[_k] = _p._$dataset(_id,_k,_v);
                });
                return _ret;
            }
// check array get
// ignore argument _value
            if (_u._$isArray(_key)){
                var _ret = {};
                _u._$forEach(_key,function(_k){
                    _ret[_k] = _p._$dataset(_id,_k);
                });
                return _ret;
            }
            return null;
        };
    /**
     * 取某个节点的属性值
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 设置成 <div id="abc" data-img="http://a.b.com/a.png">123</div>
*       // 返回value值: http://a.b.com/a.png
*       var _src = _e._$attr('abc','data-img','http://a.b.com/a.png');
*
*       // 如果设置了img的值返回data-img，否则放回空字符串
*       var _src = _e._$attr('abc','data-img');
*   });
     * ```
     *
     * @method module:base/element._$attr
     * @see    module:base/element._$dataset
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @param  {String}      arg1 - 属性名称
     * @param  {String}      arg2 - 属性值，如果没有设置此参数则表示取值
     * @return {String}             属性值
     */
    /**
     * @method CHAINABLE._$attr
     * @see module:base/element._$attr
     */
    _p._$attr =
        _y._$attr = function(_element,_name,_value){
            _element = _p._$get(_element);
            if (!_element){
                return '';
            }
            if (_value!==undefined&&!!_element.setAttribute){
                _element.setAttribute(_name,_value);
            }
            return _h.__getAttribute(_element,_name);
        };
    /**
     * html代码转节点对象，
     * 如果转换出来的节点数量超过[包含]2个，
     * 则最外面增加一个容器节点，即返回的始终是一个节点
     *
     * 结构举例
     * ```html
     *   <div id="abc">
     *     <span>123</span>
     *   </div>
     * ```
     *
     * 代码举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       var _node = _e._$html2node('<div>1</div><div><span>2</span></div>');
*   });
     * ```
     *
     * 返回结果
     * ```html
     *   <div> <!-- 返回此节点 -->
     *     <div>1</div>
     *     <div><span>2</span></div>
     *   </div>
     * ```
     *
     * @method module:base/element._$html2node
     * @param  {String} arg0 - 代码
     * @return {Node}          节点
     */
    _p._$html2node = (function(){
        var _reg = /<(.*?)(?=\s|>)/i, // first tag name
            _tmap = {li:'ul',tr:'tbody',td:'tr',th:'tr',option:'select'};
        return function(_html){
            var _tag;
            if (_reg.test(_html)){
                _tag = _tmap[(RegExp.$1||'').toLowerCase()]||'';
            }
            var _div = _p._$create(_tag||'div');
            _div.innerHTML = _html;
            var _list = _p._$getChildren(_div);
            return _list.length>1?_div:_list[0];
        };
    })();
    /**
     * 将dom节点转为xml串
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_p){
*       // 生成<div id="abc">123</div>字符串
*       var _xml = _p._$dom2xml('abc'));
*   });
     * ```
     *
     * @see    module:base/element._$xml2dom
     * @method module:base/element._$dom2xml
     * @param  {String|Node} arg0 - 节点
     * @return {String}             XML代码
     */
    /**
     * @method CHAINABLE._$dom2xml
     * @see module:base/element._$dom2xml
     */
    _p._$dom2xml =
        _y._$dom2xml = function(_element){
            _element = _p._$get(_element);
            return !_element?'':_h.__serializeDOM2XML(_element);
        };
    /**
     * 将xml转为dom节点
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 生成<div id="abc">123</div>节点
*       var _node = _e._$xml2dom('<div id="abc">123</div>');
*   });
     * ```
     *
     * @method module:base/element._$xml2dom
     * @see    module:base/element._$dom2xml
     * @param  {String} arg0 - xml文本
     * @return {Node}          DOM节点
     */
    _p._$xml2dom = function(_xml){
        _xml = (_xml||'').trim();
        return !_xml?null:_h.__parseDOMFromXML(_xml);
    };
    /**
     * dom节点转对象，多用于XML DOM转数据对象
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     *
     *   <div id="efg">
     *     <p>aaaa</p>
     *     <span>bbbb</span>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_p){
*       // 返回对象{div:'123'}
*       var _obj = _p._$dom2object('abc');
*
*       // 返回对象{div:{p:'aaaa',span:'bbbb'}}
*       var _obj = _p._$dom2object('efg');
*   });
     * ```
     *
     * @method module:base/element._$dom2object
     * @see    module:base/element._$xml2object
     * @param  {String|Node} arg0 - 节点
     * @return {Object}             转换完成的对象
     */
    /**
     * @method CHAINABLE._$dom2object
     * @see module:base/element._$dom2object
     */
    _p._$dom2object =
        _y._$dom2object = function(_dom,_obj){
            _obj = _obj||{};
            _dom = _p._$get(_dom);
            if (!_dom) return _obj;
            var _name = _dom.tagName.toLowerCase(),
                _list = _p._$getChildren(_dom);
            if (!_list||!_list.length){
                _obj[_name] = _dom.textContent||_dom.text||'';
                return _obj;
            }
            var _tmp = {};
            _obj[_name] = _tmp;
            _u._$forEach(
                _list,function(_node){
                    _p._$dom2object(_node,_tmp);
                }
            );
            return _obj;
        };
    /**
     * XML转对象
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 返回 {user:{id:'1',username:'aaa',password:'123456'}}
*       var _obj = _e._$xml2object('\
*           <?xml version="1.0" encoding="utf-8" ?>\
*           <user>\
*             <id>1</id>\
*             <username>aaa</username>\
*             <password>123456</password>\
*           </user>\
*       ');
*   });
     * ```
     *
     * @method module:base/element._$xml2object
     * @see    module:base/element._$dom2object
     * @param  {String} arg0 - xml代码
     * @return {Object}        对象
     */
    _p._$xml2object = function(_xml){
        try{
            return _p._$dom2object(_p._$xml2dom(_xml));
        }catch(ex){
            return null;
        }
    };
    /**
     * 文本转指定类型的数据
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 转成dom节点
*       var _dom = _e._$text2type('<div id="abc">123</div>',"xml");
*       // 转成json字符串
*       var _json = _e._$text2type('{"a":"aaaaaaaaaaaaa"}',"json");
*       // 原样返回
*       var _text = _e._$text2type('<div id="abc">123</div>');
*   });
     * ```
     *
     * @method module:base/element._$text2type
     * @param  {String} arg0 - 文本内容
     * @param  {String} arg1 - 类型，如xml/json/text
     * @return {Variable}      指定类型的数据
     */
    _p._$text2type = (function(){
        var _fmap = {
            xml:function(_text){
                return _p._$xml2dom(_text);
            },
            json:function(_text){
                try{
                    return JSON.parse(_text);
                }catch(ex){
                    return null;
                }
            },
            dft:function(_text){
                return _text;
            }
        };
        return function(_text,_type){
            _type = (_type||'').toLowerCase();
            return (_fmap[_type]||_fmap.dft)(_text||'');
        };
    })();
    /**
     * 批量设置节点样式
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       _e._$style('abc',{color:'red',width:'100px'});
*   });
     * ```
     *
     * 输出结果
     * ```html
     *   <div id="abc" style="color:red;width:100px;">123</div>
     * ```
     *
     * @method module:base/element._$style
     * @see    module:base/element._$setStyle
     * @param  {String|Node} arg0 - 节点
     * @param  {Object}      arg1 - 样式信息{color:'red',width:'100px'}
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$style
     * @see module:base/element._$style
     */
    _p._$style =
        _y._$style = function(_element,_map){
            _element = _p._$get(_element);
            if (!!_element){
                _u._$loop(_map,function(_value,_name){
                    _p._$setStyle(_element,_name,_value);
                });
            }
        };
    /**
     * 设置单个样式
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       _e._$setStyle('abc','color','red');
*   });
     * ```
     *
     * 输出结果
     * ```html
     *   <div id="abc" style="color:red;">123</div>
     * ```
     *
     * @method module:base/element._$setStyle
     * @see    module:base/element._$getStyle
     * @param  {String|Node} arg0 - 节点
     * @param  {String}      arg1 - 样式名称
     * @param  {String}      arg2 - 样式值
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$setStyle
     * @see module:base/element._$setStyle
     */
    _p._$setStyle =
        _y._$setStyle = function(_element,_name,_value){
            _element = _p._$get(_element);
            if (!!_element){
                _h.__setStyleValue(
                    _element,_name,
                    _h.__processCSSText(_value)
                );
            }
        };
    /**
     * 取样式值
     *
     * 结构举例
     * ```html
     *   <div id="abc" style="color:red;">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 返回节点的颜色值red（高版本浏览器返回rgb值），如果没有返回空字符串
*       var _value = _e._$getStyle('abc','color');
*   });
     * ```
     *
     * @method module:base/element._$getStyle
     * @see    module:base/element._$setStyle
     * @param  {String|Node} arg0 - 节点
     * @param  {String}      arg1 - 样式名称
     * @return {String}             样式值
     */
    /**
     * @method CHAINABLE._$getStyle
     * @see module:base/element._$getStyle
     */
    _p._$getStyle =
        _y._$getStyle = function(_element,_name){
            _element = _p._$get(_element);
            return !_element ? '' :
                _h.__getStyleValue(
                    _element,_name
                );
        };
    /**
     * 页面注入脚本
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 注入脚本，全局执行环境
*       _e._$addScript('\
*           document.getElementById("abc").style.color = "green"\
*       ');
*   });
     * ```
     *
     * 输出结果
     * ```html
     *   <div id="abc" style="color:green;">123</div>
     * ```
     *
     * @method module:base/element._$addScript
     * @param  {String} arg0 - 脚本内���
     * @return {Void}
     */

    /**
     * 注入页面内联样式，
     * 样式支持前缀标记$&lt;vendor&gt; ，
     * 如下样式值支持3D/2D切换，优先选用3D，格式：$&lt;NAME|VALUE&gt;
     *
     * * NAME支持：scale/rotate/translate/matrix
     * * VALUE格式：x=1&y=2&z=3&a=30
     *
     *
     * 范例如$&lt;scale|a=30&gt;，各名称支持的参数列表
     *
     * | 名称              | 参数 |
     * | :--        | :-- |
     * | scale      | x,y,z |
     * | rotate     | x,y,z,a |
     * | translate  | x,y,z |
     * | matrix     | m11,m12,m13,m14,m21,m22,m23,m24,m31,m32,m33,m34,m41,m42,m43,m44 |
     *
     *
     * 结构举例
     * ```html
     *   <html>
     *    <head>
     *        <title>test</title>
     *    </head>
     *   </html>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 注入样式
*       _e._$addStyle('body{font-size:20px}');
*
*       // 注入样式支持变量
*       _e._$addStyle('\
*           .a{$<vendor>transform-origin:0 0;}\
*           .b{$<vendor>transform:$<translate|x=0&y=1&z=1>}\
*       ');
*   });
     * ```
     *
     * 输出结果
     * ```html
     *   <html>
     *    <head>
     *        <title>test</title>
     *        <style>body{font-size:20px;}</style>
     *        <style>
     *           .a{-webkit-transform-origin:0 0;}\
     *           .b{-webkit-transform:translate3d(0,1,1);}\
     *        </style>
     *    </head>
     *   </html>
     * ```
     *
     * @method module:base/element._$addStyle
     * @param  {String} arg0 - 样式内容
     * @return {Node}          样式节点
     */
    _p._$addStyle = (function(){
        var _reg = /[\s\r\n]+/gi;
        return function(_css){
            _css = (_css||'').replace(_reg,' ').trim();
            var _node = null;
            if (!!_css){
                _node = _p._$create('style');
                document.head.appendChild(_node);
                _h.__injectCSSText(
                    _node,_h.__processCSSText(_css)
                );
            }
            return _node;
        };
    })();
    /**
     * 缓存待激活样式
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 设置样式到缓存中，自动生成样式名，返回自动生成的类名#<class>
*       var _class = _e._$pushCSSText('.#<uispace>{width:300px;}');
*
*       // 把缓存中的样式内联到页面
*       _e._$dumpCSSText();
*   });
     * ```
     *
     * @method module:base/element._$pushCSSText
     * @see    module:base/element._$dumpCSSText
     * @param  {String} arg0 - 样式
     * @return {String}        样式标识
     */
    _p._$pushCSSText = (function(){
        var _reg = /#<(.*?)>/g,
            _seed = +new Date;
        return function(_css,_data){
            if (!_cspol){
                _cspol = [];
            }
            var _class = 'auto-'+_u._$uniqueID(),
                _dmap = _u._$merge({uispace:_class},_data);
            _cspol.push(
                _css.replace(_reg,function($1,$2){
                    return _dmap[$2]||$1;
                })
            );
            return _class;
        };
    })();
    /**
     * 激活缓存中的样式
     *
     * 结构举例
     * ```html
     *   <div id="abc" class="item">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 设置样式.item{width:300px;}到缓存中
*       _e._$pushCSSText('.item{width:300px;}');
*
*       // 把缓存中的样式内联到页面
*       _e._$dumpCSSText();
*   });
     * ```
     *
     * @method module:base/element._$dumpCSSText
     * @see    module:base/element._$pushCSSText
     * @return {Void}
     */
    _p._$dumpCSSText = function(){
        if (!!_cspol){
            _p._$addStyle(_cspol.join(' '));
            _cspol = null;
        }
    };
    /**
     * 追加CSS规则
     *
     * 结构举例
     * ```html
     *   <style id="abc"></style>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 设置样式.item{width:300px;}到缓存中
*       _e._$appendCSSText('node-id','.item{width:300px;}');
*   });
     * ```
     *
     * @method module:base/element._$appendCSSText
     * @see    module:base/element._$addStyle
     * @param  {Node}   arg0 - 样式节点
     * @param  {String} arg1 - 单条样式规则
     * @return {CSSRule}       样式规则对象
     */
    /**
     * @method CHAINABLE._$appendCSSText
     * @see module:base/element._$appendCSSText
     */
    _p._$appendCSSText =
        _y._$appendCSSText = function(_element,_css){
            _element = _p._$get(_element);
            return !_element ? null :
                _h.__appendCSSText(
                    _element,
                    _h.__processCSSText(_css)
                );
        };
    /**
     * 新增样式类，多个样式用空格分开
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 添加样式 fc01 fc03
*       _e._$addClassName('abc','fc01 fc03');
*   });
     * ```
     *
     * 输出结果
     * ```html
     *   <div id="abc" class="fc01 fc03">123</div>
     * ```
     *
     * @method module:base/element._$addClassName
     * @see    module:base/element._$delClassName
     * @see    module:base/element._$replaceClassName
     * @param  {String|Node} arg0 - 要操作的节点标识或者节点对象
     * @param  {String}      arg1 - 要新增的样式类名称
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$addClassName
     * @see module:base/element._$addClassName
     */
    _p._$addClassName =
        _y._$addClassName = function(_element,_class){
            _element = _p._$get(_element);
            if (!!_element){
                _h.__processClassName(
                    _element,'add',_class
                );
            }
        };
    /**
     * 删除样式类，多个样式用空格分开
     *
     * 结构举例
     * ```html
     *   <div id="abc" class="fc01 fc03">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 删除fc02 fc03样式名
*       _e._$delClassName('abc','fc02 fc03');
*   });
     * ```
     *
     * 输出结果
     * ```html
     *   <div id="abc" class="fc01">123</div>
     * ```
     *
     * @method module:base/element._$delClassName
     * @see    module:base/element._$addClassName
     * @see    module:base/element._$replaceClassName
     * @param  {String|Node} arg0 - 要操作的节点标识或者节点对象
     * @param  {String}      arg1 - 要删除的样式类名称
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$delClassName
     * @see module:base/element._$delClassName
     */
    _p._$delClassName =
        _y._$delClassName = function(_element,_class){
            _element = _p._$get(_element);
            if (!!_element){
                _h.__processClassName(
                    _element,'remove',_class
                );
            }
        };
    /**
     * 替换节点的样式类名称，多个样式用空格分隔，
     * 操作过程为先删除待删样式，再添加待添样式，因此不需要删除样式存在才添加样式
     *
     * 结构举例
     * ```html
     *   <div id="abc" class="fc01 fc03">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 替换fc02为fc05
*       // 这里不需要fc02存在
*       _e._$replaceClassName('abc','fc02','fc05');
*   });
     * ```
     *
     * 输出结果
     * ```html
     *   <div id="abc" class="fc01 fc03 fc05">123</div>
     * ```
     *
     * @method module:base/element._$replaceClassName
     * @see    module:base/element._$addClassName
     * @see    module:base/element._$delClassName
     * @param  {String|Node} arg0 - 要操作的节点标识或者节点对象
     * @param  {String}      arg1 - 要删除的样式类名称
     * @param  {String}      arg2 - 要新增的样式类名称
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$replaceClassName
     * @see module:base/element._$replaceClassName
     */
    _p._$replaceClassName =
        _y._$replaceClassName = function(_element,_del,_add){
            _element = _p._$get(_element);
            if (!!_element){
                _h.__processClassName(
                    _element,'replace',
                    _del,_add
                );
            }
        };
    /**
     * 检测节点是否包含指定样式，多个样式用空格分隔，检测时包含其中之一即表示包含
     *
     * 结构举例
     * ```html
     *   <div id="abc" class="fc01 fc03">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 如果有fc01样式返回true，否则返回false
*       _e._$hasClassName('abc',"fc01");
*   });
     * ```
     *
     * @method module:base/element._$hasClassName
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @param  {String}      arg1 - 样式串
     * @return {Boolean}            是否含指定样式
     */
    /**
     * @method CHAINABLE._$hasClassName
     * @see module:base/element._$hasClassName
     */
    _p._$hasClassName =
        _y._$hasClassName = function(_element,_class){
            _element = _p._$get(_element);
            if (!!_element){
                return _h.__hasClassName(_element,_class);
            }
            return !1;
        };
    /**
     * 取样式变换矩阵对象
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 生成下面矩阵的对象
*       // |a:1,b:0,c:0,d:1,e:0:f:0|
*       // |m11:1,m12:0,m13:0,m14:0|
*       // |m21:0,m22:1,m23:0,m24:0|
*       // |m31:0,m32:0,m33:1,m34:0|
*       // |m41:0,m42:0,m43:0,m44:1|
*       var _matrix = _e._$matrix("matrix(1,0,0,1,0,0)");
*   });
     * ```
     *
     * @method module:base/element._$matrix
     * @param  {String} arg0 - 变化信息
     * @return {CSSMatrix}     变换矩阵对象
     */
    _p._$matrix = function(_matrix){
        _matrix = (_matrix||'').trim();
        return _h.__getCSSMatrix(_matrix);
    };
    /**
     * 设置3D变换，对于不支持3D的系统自动切换为2D变换
     *
     * 结构举例
     * ```html
     *   <div id="abc"></div>
     * ```
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/element'
     *   ],function(_e){
*       // 进行css3d变换，对应css样式为-webkit-transform:rotate3d( 2, 1, 1, -75deg);
*       _e._$css3d('abc','rotate',{x:2,y:1,z:1,a:'-75deg'});
*   });
     * ```
     *
     * @method module:base/element._$css3d
     * @see    module:base/element._$addStyle
     * @param  {String|Node} arg0 - 节点标识或者对象
     * @param  {String}      arg1 - 变换类型，matrix/translate/scale/rotate
     * @param  {Object}      arg2 - 变换值，{x:1,y:2,z:3,a:'30deg'}
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$css3d
     * @see module:base/element._$css3d
     */
    _p._$css3d =
        _y._$css3d = function(_element,_name,_map){
            _element = _p._$get(_element);
            if (!!_element){
                var _value = _h.__processTransformValue(_name,_map);
                if (!!_value){
                    _p._$setStyle(_element,'transform',_value);
                }
            }
        };
// for chainable
    _x._$merge(_y);
    if (CMPT){
        NEJ.copy(NEJ.P('nej.e'),_p);
    }
    return _p;
},14,20,2,3,18,21);
I$(26,function (_u,_m,_p,_o,_f,_r){
    /**
     * 验证事件信息
     * @param  {Node}     节点
     * @param  {String}   事件类型
     * @param  {Function} 处理函数
     * @return {Object}   验证后事件信息 type/handler
     */
    _p.__checkEvent = (function(){
// need change event name
        var _tmap = {
                touchstart:'mousedown',
                touchmove:'mousemove',
                touchend:'mouseup'
            },
// need prefix
            _pfix = _m._$KERNEL.prefix,
            _emap = {
                transitionend:'TransitionEnd',
                animationend:'AnimationEnd',
                animationstart:'AnimationStart',
                animationiteration:'AnimationIteration',
                visibilitychange:'visibilitychange'
            };
        var _fmap = {
            enter:function(_element,_type,_handler){
                var _result = {
                    type:'keypress'
                };
                if (!!_handler){
                    _result.handler = function(_event){
                        if (_event.keyCode===13){
                            _handler.call(_element,_event);
                        }
                    };
                }
                return _result;
            }
        };
        var _doPrefix = function(_name){
            return (_pfix.evt||_pfix.pro)+_name;
        };
        return function(_element,_type,_handler){
            var _result = {
                type:_type,
                handler:_handler
            };
            if (!(('on'+_type) in _element)){
// check name convert
                var _name = _tmap[_type];
                if (!!_name){
                    _result.type = _name;
                    return _result;
                }
// check prefix complete
                var _name = _emap[_type];
                if (!!_name){
                    _result.type = _doPrefix(_name);
                    return _result;
                }
// check event update
                var _func = _fmap[_type];
                if (!!_func){
                    return _func.apply(null,arguments);
                }
            }
            return _result;
        };
    })();
    /**
     * 添加事件
     * @param  {Node}     节点
     * @param  {String}   事件
     * @param  {Function} 处理函数
     * @param  {Boolean}  是否捕捉阶段
     * @return {Void}
     */
    _p.__addEvent = function(){
        var _args = arguments;
        if (DEBUG){
            if (!(('on'+_args[1]) in _args[0])){
                console.log('not support event['+_args[1]+'] for '+_args[0]);
            }
        }
        _args[0].addEventListener(
            _args[1],_args[2],_args[3]
        );
    };
    /**
     * 删除事件
     * @param  {Node}     节点
     * @param  {String}   事件
     * @param  {Function} 处理函数
     * @param  {Boolean}  是否捕捉阶段
     * @return {Void}
     */
    _p.__delEvent = function(){
        var _args = arguments;
        _args[0].removeEventListener(
            _args[1],_args[2],_args[3]
        );
    };
    /**
     * 触发对象的某个事件
     * @param  {String|Node} 节点ID或者对象
     * @param  {String}      鼠标事件类型
     * @return {Void}
     */
    _p.__dispatchEvent = function(_element,_type,_options){
        var _event = document.createEvent('Event');
        _event.initEvent(_type,!0,!0);
        _u._$merge(_event,_options);
        _element.dispatchEvent(_event);
    };
    return _p;
},2,17);
I$(19,function(_h,_u,_p_,_p,_o,_f,_r){var _k_ = (CMPT?NEJ.P("nej.p"):arguments[2])._$KERNEL;if (_k_.engine=='trident'&&_k_.release>='6.0'){(function (){
    /**
     * 验证事件信息
     * @param  {Node}     节点
     * @param  {String}   事件类型
     * @param  {Function} 处理函数
     * @return {Object}   验证后事件信息 type/handler
     */
    _h.__checkEvent = (function(){
        var _emap = {
            touchcancel:'MSPointerCancel',
            touchstart:'MSPointerDown',
            touchmove:'MSPointerMove',
            touchend:'MSPointerUp'
        };
        return _h.__checkEvent._$aop(function(_event){
            var _args = _event.args;
// check event convert
            var _name = _emap[_args[1]];
            if (!!_name){
                _event.stopped = !0;
                _event.value = {
                    type:_name,
                    handler:_args[2]
                };
            }
        });
    })();
})();}
    if (_k_.engine=='trident'&&_k_.release=='5.0'){(function (){
        /**
         * 验证事件信息
         * @param  {Node}     节点
         * @param  {String}   事件类型
         * @param  {Function} 处理函数
         * @return {Object}   验证后事件信息 type/handler
         */
        _h.__checkEvent = (function(){
            var _vmap = {};
            var _fmap = {
                input:function(_element,_type,_handler){
// for check type only
                    if (!_handler){
                        return {type:_type};
                    }
// fix input backspace/delete/ctrl+x bug
                    return {
                        type:_type,
                        handler:function(_event){
                            var _id = _element.id;
                            _vmap[_id] = _element.value;
                            _handler.call(_element,_event);
                        },
                        link:[[
                            document,'selectionchange',
                            function(_event){
                                var _id = _element.id;
                                if (_element!=document.activeElement){
                                    delete _vmap[_id];
                                    return;
                                }
                                if (_vmap[_id]!==_element.value){
                                    _vmap[_id] = _element.value;
                                    _handler.call(_element,_event);
                                }
                            }
                        ]]
                    };
                }
            };
            return _h.__checkEvent._$aop(function(_event){
                var _args = _event.args;
// check event update
                var _func = _fmap[_args[1]];
                if (!!_func){
                    _event.stopped = !0;
                    _event.value = _func.apply(null,_args);
                }
            });
        })();
    })();}
    if (_k_.engine=='trident'&&_k_.release>='5.0'){(function (){
// must use attach/detach for event
        var _attached = {
            'propertychange':1
        };
        /**
         * 添加事件
         * @param  {Node}     节点
         * @param  {String}   事件
         * @param  {Function} 处理函数
         * @param  {Boolean}  是否捕捉阶段
         * @return {Void}
         */
        _h.__addEvent =
            _h.__addEvent._$aop(function(_event){
                var _args = _event.args;
                if (_attached[_args[1]]!=null&&!!_args[0].attachEvent){
                    _event.stopped = !0;
                    _args[0].attachEvent('on'+_args[1],_args[2]);
                }
            });
        /**
         * 删除事件
         * @param  {Node}     节点
         * @param  {String}   事件
         * @param  {Function} 处理函数
         * @param  {Boolean}  是否捕捉阶段
         * @return {Void}
         */
        _h.__delEvent =
            _h.__delEvent._$aop(function(_event){
                var _args = _event.args,
                    _alias = _attached[_args[1]];
                if (_attached[_args[1]]!=null&&!!_args[0].detachEvent){
                    _event.stopped = !0;
                    _args[0].detachEvent('on'+_args[1],_args[2]);
                }
            });
    })();}
    if (_k_.engine=='trident'&&_k_.release<='4.0'){(function (){
        /**
         * 验证事件信息
         * @param  {Node}     节点
         * @param  {String}   事件类型
         * @param  {Function} 处理函数
         * @return {Object}   验证后事件信息 type/handler
         */
        _h.__checkEvent = (function(){
            var _lmap = {};
            var _fmap = {
                input:function(_element,_type,_handler){
                    var _result = {
                        type:'propertychange'
                    };
                    if (!!_handler){
                        _result.handler = function(_event){
// for input.value or textarea.value
                            if (('value' in _element)&&
                                _event.propertyName=='value'){
                                var _id = _element.id;
// lock cycle trigger
                                if (!!_lmap[_id]){
                                    return;
                                }
                                _lmap[_id] = !0;
                                _handler.call(_element,_event);
                                delete _lmap[_id];
                            }
                        };
                    }
                    return _result;
                },
                load:function(_element,_type,_handler){
                    var _result = {
                        type:'readystatechange'
                    };
                    if (!!_handler){
                        _result.handler = function(_event){
                            if (_element.readyState=='loaded'||
                                _element.readyState=='complete'){
                                _handler.call(_element,_event);
                            }
                        };
                    }
                    return _result;
                }
            };
            return _h.__checkEvent._$aop(function(_event){
                var _args = _event.args;
// check event update
                var _func = _fmap[_args[1]];
                if (!!_func){
                    _event.stopped = !0;
                    _event.value = _func.apply(null,_args);
                }
// use element for this in handler
                if (!!_args[2]){
                    _args[2] = _args[2]._$bind(_args[0]);
                }
            });
        })();
        /**
         * 添加事件
         * @param  {Node}     节点
         * @param  {String}   事件
         * @param  {Function} 处理函数
         * @param  {Boolean}  是否捕捉阶段
         * @return {Void}
         */
        _h.__addEvent = function(){
            var _args = arguments;
            if (DEBUG){
                if (!(('on'+_args[1]) in _args[0])){
                    console.log('not support event['+_args[1]+'] for '+_args[0]);
                }
            }
            _args[0].attachEvent('on'+_args[1],_args[2]);
        };
        /**
         * 删除事件
         * @param  {Node}     节点
         * @param  {String}   事件
         * @param  {Function} 处理函数
         * @param  {Boolean}  是否捕捉阶段
         * @return {Void}
         */
        _h.__delEvent = function(){
            var _args = arguments;
            _args[0].detachEvent('on'+_args[1],_args[2]);
        };
        /**
         * 触发对象的某个事件
         * @param  {String|Node} 节点ID或者对象
         * @param  {String}      鼠标事件类型
         * @return {Void}
         */
        _h.__dispatchEvent = (function(){
            var _omap = {
                propertychange:{propertyName:'value'}
            };
            return function(_element,_type,_options){
                var _event = document.createEventObject();
                try{
                    _u._$merge(_event,_omap[_type],_options);
                    _element.fireEvent('on'+_type,_event);
                }catch(ex){
// ignore unrecognized event name
                    console.error(ex.message);
                    console.error(ex.stack);
                }
            };
        })();
    })();}
    if (_k_.engine=='gecko'){(function (){
        /**
         * 验证事件信息
         * @param  {Node}     节点
         * @param  {String}   事件类型
         * @param  {Function} 处理函数
         * @return {Object}   验证后事件信息 type/handler
         */
        _h.__checkEvent = (function(){
            var _nreg = /^(?:transitionend|animationend|animationstart|animationiteration)$/i;
            var _fmap = {
                mousewheel:function(_element,_type,_handler){
                    var _result = {
                        type:'MozMousePixelScroll'
                    };
                    if (!!_handler){
                        _result.handler = function(_event){
                            var _delta = _event.detail;
                            _event.wheelDelta = -_delta;
                            _event.wheelDeltaY = -_delta;
                            _event.wheelDeltaX = 0;
                            _handler.call(_element,_event);
                        };
                    }
                    return _result;
                }
            };
            return _h.__checkEvent._$aop(function(_event){
                var _args = _event.args;
// check animation event
                if (_nreg.test(_args[1])){
                    _event.stopped = !0;
                    _event.value = {
                        type:_args[1],
                        handler:_args[2]
                    };
                }
// check event update
                var _func = _fmap[_args[1]];
                if (!!_func){
                    _event.stopped = !0;
                    _event.value = _func.apply(null,_args);
                }
            });
        })();
    })();};return _h;
},26,2,17);
I$(3,function (NEJ,_e,_u,_x,_h,_p,_o,_f,_r){
// {id:{type:[{type:'click',func:function,sfun:function,capt:true},...]}}
// id   - element id
// type - event name, no on prefix
// func - event after wrapper
// capt - capture flag
// sfun - event before wrapper
// link - events link to this event [[element,type,handler,capture],...]
    var _xcache = {},
        _y = {}; // chainable methods
    /*
     * 取事件类型列表
     * @param  {String} 事件类型
     * @return {Array}  事件列表
     */
    var _getTypeList = (function(){
        var _reg = /[\s,;]+/;
        return function(_type){
            var _type = (_type||'').trim().toLowerCase();
            return !_type?null:_type.split(_reg);
        };
    })();
    /*
     * 取鼠标相对于BODY的偏移
     * @param  {Event}  事件对象
     * @param  {String} 类型，X/Y
     * @param  {String} 滚动偏移名称，Left/Top
     * @return {Void}
     */
    var _getClientOffset = function(_event,_type,_name){
        var _key1 = 'page'+_type;
        return _event[_key1]!=null?_event[_key1]:(
        _event['client'+_type]+
        _e._$getPageBox()['scroll'+_name]
        );
    };
    /*
     * 取鼠标相对于页面的偏移
     * @param  {Event}  事件对象
     * @param  {String} 类型，X/Y
     * @param  {String} 滚动偏移名称，Left/Top
     * @return {Void}
     */
    var _getPageOffset = function(_event,_type,_name){
        var _key3 = 'scroll'+_name;
        _node = _p._$getElement(_event),
            _xret = _getClientOffset(_event,_type,_name);
        while(!!_node&&
        _node!=document.body&&
        _node!=document.documentElement){
            _xret += _node[_key3]||0;
            _node = _node.parentNode;
        }
        return _xret;
    };
    /*
     * 格式化添加删除事件接口参数
     * @param  {String|Node} 节点ID或者对象
     * @param  {String}      事件类型，不带on前缀，不区分大小写，多个事件用空格分隔
     * @param  {Function}    事件处理函数
     * @param  {Boolean}     是否捕获阶段事件，IE低版本浏览器忽略此参数
     * return  {Object}      格式化后参数
     */
    var _doFormatArgs = function(_element,_type,_handler,_capture){
        var _result = {};
// check element
        _element = _e._$get(_element);
        if (!_element){
            return null;
        }
        _e._$id(_element);
        _result.element = _element;
// check event handler
        if (!_u._$isFunction(_handler)){
            return null;
        }
        _result.handler = _handler;
// check type
        var _type = _getTypeList(_type);
        if (!_type){
            return null;
        }
// save info
        _result.type = _type;
        _result.capture = !!_capture;
        return _result;
    };
    /**
     * 节点添加事件，
     * 支持添加自定义事件，
     * 对于自定义事件的实现逻辑由其他模块负责实现
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 添加系统预定义事件
*       _v._$addEvent(
*           'abc','mouseover',function(_event){
*               // TODO something
*           },false
*       );
*
*       // 添加自定义事件，回车事件
*       _v._$addEvent(
*           'abc','enter',function(_event){
*               // TODO something
*           },false
*       );
*
*       // 添加多个事件，用空格分隔
*       _v._$addEvent(
*           'abc','mouseover click mousedown',
*           function(_event){
*               // TODO something
*           },false
*       );
*   });
     * ```
     *
     * 带自定义事件的类构造或者对象
     * ```javascript
     * NEJ.define([
     *     'base/klass',
     *     'base/event',
     *     'util/event',
     *     'util/event/event'
     * ],function(_k,_v,_t0,_t1,_p){
*     // 定义类
*     _p._$$Klass = _k._$klass();
*     var _pro = _p._$$Klass._$extend(_t0._$$EventTarget);
*
*     // TODO
*
*     // 添加自定义事件支持
*     // 对节点的事件同样支持此自定义事件
*     _t1._$$CustomEvent._$allocate({
*         element:_p._$$Klass,
*         event:['ok','fail']
*     });
*
*     // 使用事件接口添加/删除/调度事件
*     var _handler = function(_event){
*         // TODO
*     };
*     _v._$addEvent(_p._$$Klass,'ok',_handler);
*     _v._$delEvent(_p._$$Klass,'ok',_handler);
* });
     * ```
     *
     * @method module:base/event._$addEvent
     * @see    module:base/event._$delEvent
     * @param  {String|Node|Object} arg0 - 节点或者类构造或者对象
     * @param  {String}      arg1 - 事件类型，不带on前缀，不区分大小写，多个事件用空格分隔
     * @param  {Function}    arg2 - 事件处理函数
     * @param  {Boolean}     arg3 - 是否捕获阶段事件，IE低版本浏览器忽略此参数
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$addEvent
     * @see module:base/event._$addEvent
     */
    _p._$addEvent =
        _y._$addEvent = (function(){
// cache event
// type/handler/link
            var _doCacheEvent = function(_type,_source,_real){
                var _id = _e._$id(_source.element),
                    _cch_id = _xcache[_id]||{},
                    _cch_tp = _cch_id[_type]||[];
                _cch_tp.push({
                    type:_real.type||_type,
                    func:_real.handler||_source.handler,
                    sfun:_source.handler,
                    capt:_source.capture,
                    link:_real.link
                });
                _cch_id[_type] = _cch_tp;
                _xcache[_id] = _cch_id;
            };
            return function(){
                var _args = _doFormatArgs.apply(null,arguments);
                if (!_args) return;
                _u._$forEach(
                    _args.type,function(_name){
                        var _argc = _h.__checkEvent(
                            _args.element,
                            _name,_args.handler
                        );
// add event
                        _h.__addEvent(
                            _args.element,_argc.type,
                            _argc.handler,_args.capture
                        );
// add event link
                        _u._$forIn(
                            _argc.link,function(_item){
                                _item[3] = !!_item[3];
                                _h.__addEvent.apply(_h,_item);
                                _item[0] = _e._$id(_item[0]);
                            }
                        );
// cache event
                        _doCacheEvent(_name,_args,_argc);
                    }
                );
            };
        })();
    /**
     * 节点删除事件，输入参数必须保证与添加接口_$addEvent输入参数完全一致
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 事件回调业务逻辑
*       var _doCallback = function(_event){
*           // TODO something
*           alert('0');
*       };
*
*       // 添加事件
*       _v._$addEvent('abc','mouseover',_doCallback,false);
*       // 删除事件，这里参数必须保持完全一致
*       _v._$delEvent('abc','mouseover',_doCallback,false);
*
*       // 比如以下方式虽然回调的业务逻辑一致，但是无法删除之前添加的事件
*       _v._$delEvent(
*           'abc',"mouseover",function(_event){
*               // TODO something
*               alert('0');
*           },false
*       );
*
*       // 删除多个事件
*       _v._$delEvent(
*           'abc','mouseover click mouseup',
*           _doCallback,false
*       );
*   });
     * ```
     *
     * @method module:base/event._$delEvent
     * @see    module:base/event._$addEvent
     * @param  {String|Node} arg0 - 节点ID或者对象
     * @param  {String}      arg1 - 事件类型，不带on前缀，不区分大小写，多个事件用空格分隔
     * @param  {Function}    arg2 - 事件处理函数
     * @param  {Boolean}     arg3 - 是否捕获阶段事件
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$delEvent
     * @see module:base/event._$delEvent
     */
    _p._$delEvent =
        _y._$delEvent = (function(){
            var _unCacheEvent = function(_type,_conf){
                var _id = _e._$id(_conf.element),
                    _cch_id = _xcache[_id]||_o,
                    _cch_tp = _cch_id[_type],
                    _index = _u._$indexOf(
                        _cch_tp,function(_item){
// check handler and capture
                            return _item.sfun===_conf.handler&&
                                _item.capt===_conf.capture;
                        }
                    );
// check result
                var _result = null;
                if (_index>=0){
                    var _item = _cch_tp.splice(_index,1)[0];
                    _result = [[
                        _conf.element,_item.type,
                        _item.func,_conf.capture
                    ]];
                    if (!!_item.link){
                        _result.push.apply(_result,_item.link);
                    }
// clear cache
                    if (!_cch_tp.length){
                        delete _cch_id[_type];
                    }
                    if (!_u._$hasProperty(_cch_id)){
                        delete _xcache[_id];
                    }
                }
                return _result;
            };
            return function(){
                var _args = _doFormatArgs.apply(null,arguments);
                if (!_args) return;
                _u._$forEach(
                    _args.type,function(_name){
                        _u._$forEach(
                            _unCacheEvent(_name,_args),
                            function(_item){
                                _h.__delEvent.apply(_h,_item);
                            }
                        );
                    }
                );
            };
        })();
    /**
     * 清除节点事件
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 添加事件
*       _v._$addEvent(
*           'abc','mouseover',function(_event){
*               // TODO something
*           }
*       );
*       _v._$addEvent(
*           'abc','mouseover',function(_event){
*               // TODO something
*           },true
*       );
*       _v._$addEvent(
*           'abc','custom',function(_event){
*               // TODO something
*           }
*       );
*
*       // 清除节点所有事件，包括两个mouseover事件和一个custom事件
*       _v._$clearEvent('abc');
*
*       // 清除节点指定类型事件，只清除两个mouseover事件
*       _v._$clearEvent('abc','mouseover');
*
*       // 清除多个事件，用空格分隔
*       _v._$clearEvent('abc','mouseover custom');
*   });
     * ```
     *
     * @method module:base/event._$clearEvent
     * @see    module:base/event._$delEvent
     * @param  {String|Node} arg0 - 节点ID或者对象
     * @param  {String}      arg1 - 事件类型，不带on前缀，不区分大小写，多个事件用空格分隔
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$clearEvent
     * @see module:base/event._$clearEvent
     */
    _p._$clearEvent =
        _y._$clearEvent = (function(){
            var _doClearEvent = function(_id,_name,_list){
                _u._$reverseEach(
                    _list,function(_item){
                        _p._$delEvent(
                            _id,_name,_item.sfun,_item.capt
                        );
                    }
                );
            };
            return function(_element,_type){
                var _id = _e._$id(_element);
                if (!_id) return;
                var _cch_id = _xcache[_id];
                if (!!_cch_id){
                    _type = _getTypeList(_type);
                    if (!!_type){
// clear event by type
                        _u._$forEach(
                            _type,function(_name){
                                _doClearEvent(_id,_name,_cch_id[_name]);
                            }
                        );
                    }else{
// clear all event
                        _u._$loop(
                            _cch_id,function(_value,_name){
                                _p._$clearEvent(_element,_name);
                            }
                        );
                    }
                }
            };
        })();
    /**
     * 触发对象的某个事件，注：对于IE浏览器该接口节点事件有以下限制
     *
     * * 捕获阶段支持需要浏览器IE9+
     * * 节点上自定义事件支持需要浏览器IE9+
     *
     *
     * 结构举例
     * ```html
     *   <div id="abc">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 注册鼠标事件
*       _v._$addEvent(
*           'abc','click',function(_event){
*               // 获取鼠标事件触发的垂直位置
*               var _y = _v._$pageY(_event);
*           }
*       );
*       // 触发鼠标事件
*       _v._$dispatchEvent('abc','click');
*
*       // 注册自定义事件
*       _v._$addEvent(
*           'abc','ok',function(_event){
*               // TODO something
*           }
*       );
*       // 触发自定义事件
*       _v._$dispatchEvent('abc','ok');
*   });
     * ```
     *
     * @method module:base/event._$dispatchEvent
     * @param  {String|Node} arg0 - 节点ID或者对象
     * @param  {String}      arg1 - 鼠标事件类型，不区分大小写，多个事件用空格分隔
     * @param  {Object}      arg2 - 传递的参数信息
     * @return {Void}
     */
    /**
     * @method CHAINABLE._$dispatchEvent
     * @see module:base/event._$dispatchEvent
     */
    _p._$dispatchEvent =
        _y._$dispatchEvent = function(_element,_type,_options){
            var _element = _e._$get(_element);
            if (!!_element){
                _u._$forEach(
                    _getTypeList(_type),function(_name){
                        var _result = _h.__checkEvent(
                            _element,_name
                        );
                        _h.__dispatchEvent(
                            _element,_result.type,_options
                        );
                    }
                );
            }
        };
    /**
     * 获取触发事件的节点，可以传入过滤接口来遍历父节点找到符合条件的节点
     *
     * 结构举例
     * ```html
     *   <div id="a">
     *     <p>
     *       <span id="b">123</span>
     *       <span link="a">123</span>
     *       <span class="a link">123</span>
     *       <span data-link="a">123</span>
     *       <label>aaaaa</label>
     *     </p>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 取事件触发节点
*       _v._$addEvent(
*           'b','click',function(_event){
*               // id为b的节点
*               var _node = _v._$getElement(_event);
*               // TODO something
*           }
*       );
*
*       // 事件触发，取id是a的节点
*       _v._$addEvent(
*           'b','click',function(_event){
*               // id为a的节点
*               var _node = _v._$getElement(
*                   _event,function(_element){
*                       return _element.id=='a';
*                   }
*               );
*               // TODO something
*
*               // class含link或者属性含link或者data-link的节点
*               var _node = _v._$getElement(_event,'link');
*
*               // 仅匹配class即 class="link xx xxx"
*               var _node = _v._$getElement(_event,'c:link');
*
*               // 仅匹配dataset即 data-link="aaaa"
*               var _node = _v._$getElement(_event,'d:link');
*
*               // 仅匹配attributer即 link="aaa"
*               var _node = _v._$getElement(_event,'a:link');
*
*               // 仅匹配tag即 <label>
*               var _node = _v._$getElement(_event,'t:label');
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$getElement
     * @param  {Event}    arg0 - 事件对象
     * @param  {Function} arg1 - 过滤接口
     * @return {Node}            符合条件的节点
     */
    _p._$getElement = (function(){
// element filter
        var _exmap;
        var _doFilter = function(_name,_element){
            var _arr = _name.split(':');
            if (_arr.length>1){
                if (!_exmap){
                    _exmap = {
                        a:_e._$attr,
                        d:_e._$dataset,
                        c:_e._$hasClassName,
                        t:function(n,v){return (n.tagName||'').toLowerCase()===v;}
                    };
                }
                var _check = _exmap[_arr[0]];
                if (!!_check){
                    return !!_check(_element,_arr[1]);
                }
                _name = _arr[1];
            }
            return !!_e._$attr(_element,_name)||
                !!_e._$dataset(_element,_name)||
                _e._$hasClassName(_element,_name);
        };
        return function(_event){
            if (!_event) return null;
            var _element = _event.target||
                    _event.srcElement,
                _filter = arguments[1];
            if (!_filter){
                return _element;
            }
            if (_u._$isString(_filter)){
                _filter = _doFilter._$bind(null,_filter);
            }
            if (_u._$isFunction(_filter)){
                while(_element){
                    if (!!_filter(_element)){
                        return _element;
                    }
                    _element = _element.parentNode;
                }
                return null;
            }
            return _element;
        };
    })();
    /**
     * 阻止事件，包括默认事件和传递事件
     *
     * 结构举例
     * ```html
     *   <div id="a">
     *     <a href="xxx.html" id="b">123</a>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 事件回调中阻止事件冒泡
*       _v._$addEvent(
*           'b','click',function(_event){
*               // 阻止事件继续传播
*               // 阻止链接打开的默认事件
*               _v._$stop(_event);
*           }
*       );
*
*       // a节点上的点击事件不会触发
*       _v._$addEvent(
*           'a','click',function(_event){
*               alert(0);
*               // TODO something
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$stop
     * @see    module:base/event._$stopBubble
     * @see    module:base/event._$stopDefault
     * @param  {Event} arg0 - 要阻止的事件对象
     * @return {Void}
     */
    _p._$stop = function(_event){
        _p._$stopBubble(_event);
        _p._$stopDefault(_event);
    };
    /**
     * 阻止事件的冒泡传递
     *
     * 结构举例
     * ```html
     *   <div id="a">
     *     <a href="xxx.html" id="b">123</a>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 事件回调中阻止事件冒泡
*       _v._$addEvent(
*           'b','click',function(_event){
*               // 阻止事件继续传播
*               // 链接仍然会被打开
*               _v._$stopBubble(_event);
*           }
*       );
*
*       // a节点上的点击事件不会触发
*       _v._$addEvent(
*           'a','click',function(_event){
*               alert(0);
*               // TODO something
*           }
*       );
*   });
     * ```
     *
     * @see    module:base/event._$stop}
     * @method module:base/event._$stopBubble
     * @param  {Event} arg0 - 要阻止的事件对象
     * @return {Void}
     */
    _p._$stopBubble = function(_event){
        if (!!_event){
            !!_event.stopPropagation
                ? _event.stopPropagation()
                : _event.cancelBubble = !0;
        }
    };
    /**
     * 阻止标签的默认事件
     *
     * 结构举例
     * ```html
     *   <div id="a">
     *     <a href="xxx.html" id="b">123</a>
     *   </div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 事件回调中阻止链接默认事件
*       _v._$addEvent(
*           'b','click',function(_event){
*               // 阻止链接打开页面的默认行为
*               _v._$stopDefault(_event);
*           }
*       );
*
*       // a节点上的点击事件仍然会触发
*       _v._$addEvent(
*           'a','click',function(_event){
*               alert(0);
*               // TODO something
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$stopDefault
     * @see    module:base/event._$stop
     * @param  {Event} arg0 - 要阻止的事件对象
     * @return {Void}
     */
    _p._$stopDefault = function(_event) {
        if (!!_event){
            !!_event.preventDefault
                ? _event.preventDefault()
                : _event.returnValue = !1;
        }
    };
    /**
     * 取事件相对于页面的位置
     *
     * 结构举例
     * ```html
     *   <div id="abc" style="width:100%;height:100%;">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 回调中取鼠标位置
*       _v._$addEvent(
*           'abc','click',function(_event){
*               // 获取鼠标事件触发的水平、垂直位置
*               var _pos = _v._$page(_event);
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$page
     * @see    module:base/event._$pageX
     * @see    module:base/event._$pageY
     * @param  {Event}  arg0 - 事件对象
     * @return {Object}        位置信息，{x:10,y:10}
     */
    _p._$page = function(_event){
        return {
            x:_p._$pageX(_event),
            y:_p._$pageY(_event)
        };
    };
    /**
     * 取事件相对于页面左侧的位置，累加所有内部滚动高度
     *
     * 结构举例
     * ```html
     *   <div id="abc" style="width:100%;height:100%;">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 回调中取鼠标位置
*       _p._$addEvent(
*           'abc','click',function(_event){
*               // 获取鼠标事件触发的水平位置
*               var _x = _v._$pageX(_event);
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$pageX
     * @see    module:base/event._$clientX
     * @param  {Event}  arg0 - 事件对象
     * @return {Number}        水平位置
     */
    _p._$pageX = function(_event){
        return _getPageOffset(_event,'X','Left');
    };
    /**
     * 取事件相对于页面顶部的位置，累加所有内部滚动高度
     *
     * 结构举例
     * ```html
     *   <div id="abc" style="width:100%;height:100%;">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 回调中取鼠标位置
*       _v._$addEvent(
*           'abc','click',function(_event){
*               // 获取鼠标事件触发的垂直位置
*               var _y = _v._$pageY(_event);
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$pageY
     * @see    module:base/event._$clientY
     * @param  {Event}  arg0 - 事件对象
     * @return {Number}        垂直位置
     */
    _p._$pageY = function(_event){
        return _getPageOffset(_event,'Y','Top');
    };
    /**
     * 取事件相对于页面左侧的位置，仅累加页面滚动高度
     *
     * 结构举例
     * ```html
     *   <div id="abc" style="width:100%;height:100%;">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 回调中取鼠标位置
*       _p._$addEvent(
*           'abc','click',function(_event){
*               // 获取鼠标事件触发的水平位置
*               var _x = _v._$clientX(_event);
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$clientX
     * @see    module:base/event._$pageX
     * @param  {Event}  arg0 - 事件对象
     * @return {Number}        水平位置
     */
    _p._$clientX = function(_event){
        return _getClientOffset(_event,'X','Left');
    };
    /**
     * 取事件相对于页面顶部的位置，仅累加页面滚动高度
     *
     * 结构举例
     * ```html
     *   <div id="abc" style="width:100%;height:100%;">123</div>
     * ```
     *
     * 脚本举例
     * ```javascript
     *   NEJ.define([
     *       'base/event'
     *   ],function(_v){
*       // 回调中取鼠标位置
*       _v._$addEvent(
*           'abc','click',function(_event){
*               // 获取鼠标事件触发的垂直位置
*               var _y = _v._$pageY(_event);
*           }
*       );
*   });
     * ```
     *
     * @method module:base/event._$clientY
     * @see    module:base/event._$pageY
     * @param  {Event}  arg0 - 事件对象
     * @return {Number}        垂直位置
     */
    _p._$clientY = function(_event){
        return _getClientOffset(_event,'Y','Top');
    };
// for chainable method
    _x._$merge(_y);
    if (CMPT){
        NEJ.copy(NEJ.P('nej.v'),_p);
    }
    return _p;
},14,4,2,18,19);
I$(5,function (_ut) {
    var _ = {},
        noop = function(){},
        _userAgent = navigator.userAgent,
// IOS
        _isIOS = !!_userAgent.match(/(iPhone|iPod|iPad)/i),
// AOS
        _isAOS = !!_userAgent.match(/Android/i),
        _searchPram = location.search.replace('?',''),
        _urlObj = _ut._$query2object(_searchPram);
// 类型判断， 同typeof
    _.typeOf = function (o) {
        return o == null ? String(o) : ({}).toString.call(o).slice(8, -1).toLowerCase();
    }
    _.findInList = function(id, list, ident){
        ident = ident || "id";
        var len = list.length;
        for(; len--;){
            if(list[len][ident] == id) return len
        }
        return -1;
    }
    _.merge = function(obj1, obj2){
        var
            type1 = _.typeOf(obj1),
            type2 = _.typeOf(obj2),
            len;
        if(type1 !== type2) return obj2;
        switch(type2){
            case 'object':
                for(var i in obj2){
                    if(obj2.hasOwnProperty(i)){
                        obj1[i] = _.merge(obj1[i], obj2[i]);
                    }
                }
                break;
            case "array":
                for(var i = 0, len = obj2.length; i < len; i++ ){
                    obj1[i] = _.merge(obj1[i], obj2[i]);
                }
                obj1.length = obj2.length;
                break;
            default:
                return obj2;
        }
        return obj1;
    }  // meregeList
    _.mergeList = function(list, list2, ident){
        ident = ident || "id";
        var len = list.length;
        for(; len--;){
            for(var i = 0, len1 = list2.length; i < len1; i++){
                if(list2[i][ident] != null&&list2[i][ident] === list[len][ident]){
                    list.splice(len, 1, _.merge(list2[i],list[len]));
                    break;
                }
            }
        }
    }
// 深度clone
    _.clone = function(obj){
        var type = _.typeOf(obj);
        switch(type){
            case "object":
                var cloned = {};
                for(var i in obj){
                    cloned[i] = _.clone(obj[i])
                }
                return cloned;
            case 'array':
                return obj.map(_.clone);
            default:
                return obj;
        }
        return obj;
    }
    _.extend = function(o1, o2 ,override){
        for( var i in o2 ) if( o1[i] == undefined || override){
            o1[i] = o2[i]
        }
        return o1;
    }
    _.initSelect = function(_select,_list,_value,_text){
        _select.options.length = 0;
        _value = _value||'value';
        _text = _text||'text';
        for(var i=0,l=_list.length;i<l;i++){
            if(typeof _list[i]==='string'){
                var option = new Option(_list[i],_list[i]);
            } else{
                var option = new Option(_list[i][_text],_list[i][_value]);
            }
            _select.options.add(option);
        }
    }
// 利用一个webp图片能否显示来检测当前浏览器环境是否支持webp
// 返回true 支持，否则不支持
// added by hzliuxinqi 2015-8-11
    _._$supportWebp = (function(){
        var __supportwebp = false;
        (function(){
            var webp = new Image();
            webp.onload = webp.onerror = function() {
                __supportwebp = webp.height === 2;
                webp.onload = webp.onerror = null;
                webp = null;
            };
//高度为2的一个webp图片
            webp.src = 'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
        })();
        return function(){ return __supportwebp; };
    })();
// 获取nos压缩处理后图像的链接

// 函数执行频度控制， added by hzliuxinqi refer from underscore
    /**
     * 频率控制 返回函数连续调用时，func 执行频率限定为 次 / wait
     *
     * @param  {function}   func      传入函数
     * @param  {number}     wait      表示时间窗口的间隔
     * @param  {object}     options   如果想忽略开始边界上的调用，传入{leading: false}。
     *                                如果想忽略结尾边界上的调用，传入{trailing: false}
     * @return {function}             返回客户调用函数
     */
    _.throttle = function(func, wait, options) {
        var context, args, result;
        var timeout = null;
// 上次执行时间点
        var previous = 0;
        if (!options) options = {};
// 延迟执行函数
        var later = function() {
// 若设定了开始边界不执行选项，上次执行时间始终为0
            previous = options.leading === false ? 0 : (+new Date);
            timeout = null;
            result = func.apply(context, args);
            if (!timeout) context = args = null;
        };
        return function() {
            var now = (+new Date);
// 首次执行时，如果设定了开始边界不执行选项，将上次执行时间设定为当前时间。
            if (!previous && options.leading === false) previous = now;
// 延迟执行时间间隔
            var remaining = wait - (now - previous);
            context = this;
            args = arguments;
// 延迟时间间隔remaining小于等于0，表示上次执行至此所间隔时间已经超过一个时间窗口
// remaining大于时间窗口wait，表示客户端系统时间被调整过
            if (remaining <= 0 || remaining > wait) {
                clearTimeout(timeout);
                timeout = null;
                previous = now;
                result = func.apply(context, args);
                if (!timeout) context = args = null;
//如果延迟执行不存在，且没有设定结尾边界不执行选项
            } else if (!timeout && options.trailing !== false) {
                timeout = setTimeout(later, remaining);
            }
            return result;
        };
    };
    /**
     * 空闲控制 返回函数连续调用时，空闲时间必须大于或等于 wait，func 才会执行
     *
     * @param  {function} func        传入函数
     * @param  {number}   wait        表示时间窗口的间隔
     * @param  {boolean}  immediate   设置为ture时，调用触发于开始边界而不是结束边界
     * @return {function}             返回客户调用函数
     */
    _.debounce = function(func, wait, immediate) {
        var timeout, args, context, timestamp, result;
        var later = function() {
// 据上一次触发时间间隔
            var last = (+new Date) - timestamp;
// 上次被包装函数被调用时间间隔last小于设定时间间隔wait
            if (last < wait && last > 0) {
                timeout = setTimeout(later, wait - last);
            } else {
                timeout = null;
// 如果设定为immediate===true，因为开始边界已经调用过了此处无需调用
                if (!immediate) {
                    result = func.apply(context, args);
                    if (!timeout) context = args = null;
                }
            }
        };
        return function() {
            context = this;
            args = arguments;
            timestamp = (+new Date);
            var callNow = immediate && !timeout;
// 如果延时不存在，重新设定延时
            if (!timeout) timeout = setTimeout(later, wait);
            if (callNow) {
                result = func.apply(context, args);
                context = args = null;
            }
            return result;
        };
    };
//提供在浏览器下一帧渲染时回调的入口
//added by hzliuxinqi 2015-08-25
    _.nextFrame = (function(){
        var vendors = ['ms', 'moz', 'webkit', 'o'];
        var w = {};
        w.__requestAnimationFrame = window.requestAnimationFrame;
        for(var x = 0; x < vendors.length && !w.__requestAnimationFrame; ++x) {
            w.__requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
        }
        if (!w.__requestAnimationFrame)
            w.__requestAnimationFrame = function(callback) {
                var id = window.setTimeout(function() { callback(); }, 16);
                return id;
            };
        return function(callback){
            w.__requestAnimationFrame.apply(window, arguments);
        };
    })();



    /**
     * 获取url的search中的参数值  param具体参数的key；all若为true，返回整个urlObj对象
     * add by hzmating
     * 20150920
     */
    _.getUrlParam = function(param,all){
        if(!!all){
            return _urlObj;
        }else{
            return _urlObj[param];
        }
    };
    return _;
},2);
!function(win, doc, undefined) {
// __nes命名空间__
    var nes = function(node, context){return all(node, context);},
        locals = {}; //存放local属性...被global坑死了
// 常用属性local化
    var ap = Array.prototype,
        op = Object.prototype,
        sp = String.prototype,
        fp = Function.prototype,
        slice = ap.slice,
        body = doc.body,
        testNode = doc.createElement("div"),
// 1. Helper(助手函数)
// =================================
// 将类数组(如Nodelist、Argument)变为数组
        toArray = function(arr) {
            return slice.call(arr);
        },
// 够用的短小类型判断
        typeOf = function(o) {
            return o == null ? String(o) : op.toString.call(o).slice(8, -1).toLowerCase();
        },
// 够用的简单对象扩展
        extend = function(o1, o2, override) {
            for (var i in o2) {
                if (o1[i] == null || override) o1[i] = o2[i];
            }
        },
// 最简单先进先出缓存队列, max设置最大缓存长度, 为了不必要重复parse
// nes会多次用到这个方法创建cache
        createCache = function(max) {
            var keys = [],
                cache = {};
            return {
                set: function(key, value) {
                    if (keys.length > this.length) {
                        delete cache[keys.shift()];
                    }
                    cache[key] = value;
                    keys.push(key);
                    return value;
                },
                get: function(key) {
                    if (key === undefined) return cache;
                    return cache[key];
                },
                length: max,
                len: function() {
                    return keys.length;
                }
            };
        },
// 让setter型函数fn支持object型的参数
// 即支持`set(name:value)`
// 也支持`set({name1:value1,name2:value2})`
        autoSet = function(fn) {
            return function(key, value) {
                if (typeOf(key) == "object") {
                    for (var i in key) {
                        fn.call(this, i, key[i]);
                    }
                } else {
                    fn.call(this, key, value);
                }
                return this;
            };
        },
        assert = function(fn) {
            try {
                return fn();
            } catch (e) {
                return false;
            } finally {
                testNode = document.createElement("div");
            }
        };
// Fixed: toArray 低于IE8的 Nodelist无法使用slice获得array
    try {
        slice.call(doc.getElementsByTagName("body"));
    } catch (e) {
        toArray = function(arr) {
            var result = [],
                len = arr.length;
            for (var i = 0; i < len; i++) {
                result.push(arr[i]);
            }
            return result;
        };
    }
// 扩展ES5 Native支持的函数，坑爹的远古浏览器
//es5 trim
    var trimReg = /^\s+|\s+$/g;
    sp.trim = sp.trim ||
    function() {
        return this.replace(trimReg, "");
    };
//es5 bind
    fp.bind = fp.bind ||
    function(context, args) {
        args = slice.call(arguments, 1);
        var fn = this;
        return function() {
            return fn.apply(context, args.concat(slice.call(arguments)));
        };
    };
//es5 Array indexOf
    ap.indexOf = ap.indexOf ||
    function(a) {
        for (var i = 0, len = this.length; i < len; i++) {
            if (a === this[i]) return i;
        }
        return -1;
    };
// Parser 相关
    var
//抽离出字匹配数目
        ignoredRef = /\(\?\!|\(\?\:/,
        extractRefNum = function(regStr) {
            var left = 0,
                right = 0,
                len = regStr.length,
                ignored = regStr.split(ignoredRef).length - 1; //忽略非捕获匹配
            for (; len--;) {
                var letter = regStr.charAt(len);
                if (len === 0 || regStr.charAt(len - 1) !== "\\") { //不包括转义括号
                    if (letter === "(") left++;
                    if (letter === ")") right++;
                }
            }
            if (left !== right) throw regStr + "中的括号不匹配";
            else return left - ignored;
        },
//前向引用 如\1 \12 等在TRUNK合并时要做处理
        refIndexReg = /\\(\d+)/g,
        extractRefIndex = function(regStr, curIndex) {
            return regStr;
// .replace(refIndexReg, function(a, b) {
//   return "\\" + (parseInt(b, 10) + curIndex);
// });
        },
// // 生成默认的action，这个会将匹配到的参数推入一个同名的数组内
// createAction = function(name) {
//   return function(all) {
//     var parsed = this.parsed,
//       current = parsed[name] || (parsed[name] = [])
//       current.push(slice.call(arguments))
//   }
// },
// Object.keys 规则排序时的调用方法
        keys = Object.keys ||
            function(obj) {
                var result = [];
                for (var prop in obj) {
                    if (obj.hasOwnProperty(prop)) result.push(prop);
                }
                return result;
            },
// 将规则中的reg中的macro替换掉
        cleanRule = function(rule) {
            var reg = rule.reg;
//如果已经是regexp了就转为string
            if (typeOf(reg) === "regexp") reg = reg.toString().slice(1, -1);
//将macro替换
            rule.regexp = reg.replace(replaceReg, function(a, b) {
                if (b in macros) return macros[b];
                else throw new Error('can"t replace undefined macros:' + b);
            });
            return rule;
        }, cleanRules = function(rules) {
            for (var i in rules) {
                if (rules.hasOwnProperty(i)) cleanRule(rules[i]);
            }
            return rules;
        };
// ##2. Parser
//
// 为何要抽象成一个类? 其实这里只用到了一个实例
// 事实上这个简单Parser还帮我实现了命令行参数解析，
// zen-coding的实现等等, 它可以帮助实现基于正则式的
// 字符串解析
    function Parser(opts) {
        opts = opts || {};
        if (opts.macros) this._macros = opts.macros;
        this._links = {}; //symbol link map
        this._rules = {}; //symbol def
        this.TRUNK = null;
        this.cache = createCache(opts.maxCache || 200);
        this.cache.set("", [[] ]); //输入空字符串返回空数组
    }
    extend(Parser.prototype, {
// ### 解析输入字符串input、返回action定义的data数据
        parse: function(input) {
// 清理input数据、因为parsed数据最终会被缓存，
// 我们要尽量让相同的选择器只对应一份parsed数据
            input = clean(input);
// 先检查缓存中是否有数据
            if (parsed = this.cache.get(input)) return parsed;
// 如果没有: 初始化参数
            var parsed = this.parsed = [
                [null]
            ];
            var remain = this.input = input;
            var TRUNK = this.TRUNK;
            var prevRemain;
// 将remain进行this._process这里每匹配一个字符串都会进行一次reduce
            while (prevRemain != (remain = remain.replace(TRUNK, this._process.bind(this)))) {
                prevRemain = remain;
            }
// 如果没有被解析完 证明选择器字符串有不能被解析的部分
            if (remain !== '') this.error(remain);
// 返回数据并推入cache
            return this.cache.set(input, parsed);
        },
// ###添加新规则 :
// 在nes中你可以想象成添加一个与Id、className、pesudo等价简单选择符
        on: function(rules) {
            if (typeOf(rules) === "string") { //当不是hash传入时
                var tmp = {};
                tmp[rules] = arguments[1];
                rules = tmp;
            }
// 可以同时接受object型或者key, value对的参数
            for (var i in rules) {
                var rule = rules[i];
                if (typeOf(rule) !== "object") {
                    rule = {
                        regexp: rule
                    };
                }
                var reg = rule.regexp;
                if (typeOf(reg) === "regexp") {
                    rule.regexp = reg.toString().slice(1, -1);
                }
// 初始化order
                if (rule.order === undefined) rule.order = 1;
                this._rules[i] = rule;
            }
// 每进行一次新规则监听，都重新组装一次
            this.setup();
            return this;
        },
// ###__删除规则__ :
// 删除对应规则, 即nes的规则都是在运行时可删可增的
        off: function(name) {
            if (typeOf(name) === "array") {
                for (var i = name.length; i--;) {
                    this.off(name[i]);
                }
            } else {
                if (this._rules[name]) {
                    delete this._rules[name];
                }
            }
            return this;
        },
// 获得当前解析位置所在的datum，你只需要在这个datum中塞数据即可
        current: function() {
            var data = this.parsed;
            var piece = data[data.length - 1],
                len = piece.length;
            return piece[len - 1] || (piece[len - 1] = {
                    tag: "*"
                });
        },
        error: function(info) {
            throw Error("输入  " + this.input + "  含有未识别语句:" + info || "");
        },
        clone: function(parser) {
            return new Parser().on(this._rules);
        },
// __`this.parser`__的依赖方法，
// 即遍历links检查是否有子匹配满足关系，
// 有则推入对应的action数组,
// 注意由于其是是replace方法的调用，每次都要返回""完成
// reduce操作
        _process: function() {
            var links = this._links,
                rules = this._rules,
                args = slice.call(arguments);
            for (var i in links) {
                var link = links[i],
                    retain = link[1],
                    index = parseInt(link[0]);
                if (args[index] && (rule = rules[i])) {
                    rule.action.apply(this, args.slice(index, index + retain));
                    return "";
                }
            }
            return "";
        },
// 组装
        setup: function() {
            cleanRules(this._rules);
            var curIndex = 1,
//当前下标
                splits = [],
                rules = this._rules,
                links = this._links,
                ruleNames = keys(rules).sort(function(a, b) {
                    return rules[a].order >= rules[b].order;
                }),
                len = ruleNames.length;
            for (; len--;) {
                var i = ruleNames[len],
                    rule = rules[i],
                    retain = extractRefNum(rule.regexp) + 1; // 1就是那个all
                if (rule.filter && !filters[i]) {
                    filters[i] = rule.filter;
                } //将filter转移到filters下
                links[i] = [curIndex, retain]; //分别是rule名，参数数量
                var regexp = extractRefIndex(rule.regexp, curIndex - 1);
                curIndex += retain;
                splits.push(regexp);
            }
            this.TRUNK = new RegExp("^(?:(" + splits.join(")|(") + "))");
            return this;
        }
    });
// ### parse的规则定义部分开始
// 一些用到的正则式，但是又不属于parser的规则组成
    var
        replaceReg = /\{\{([^\}]*)\}\}/g,
//替换rule中的macro
        nthValueReg = /^(?:(\d+)|([+-]?\d*)?n([+-]\d+)?)$/,
// nth伪类的value规则
        posPesudoReg = /^(nth)[\w-]*(-of-type|-child)/,
//判断需要pos
// 第一个cache 用来装载nth伪类中的参数解析后的数据
// 如nth-child、nth-of-type等8个伪类
        nthCache = createCache(100),
// 提取nthValue中的有用信息 比如an + b 我们需要提取出a以及,b并对额外情况如缺少a参数或b参数
// 或者有a、b小于0这些情况作统一处理，返回find适合使用的数据
        extractNthValue = function(param) {
            var step, start, res;
//如果无参数 当成是获取第一个元素
            if (!param || !(param = param.replace(/\s+/g, ""))) {
                return {
                    start: 1,
                    step: 0
                };
            }
            if (res = nthCache.get(param)) return res;
// 对even odd等转化为标准的a，b组合(即step与start)
            if (param == "even") {
                start = 2;
                step = 2;
            } else if (param == "odd") {
                step = 2;
                start = 1;
            } else {
                res = param.match(nthValueReg);
// 对错误的nth参数抛出错误
                if (!res) step = null; // 无论其他参数，如果step为null，则永远为false
                else {
                    if (res[1]) {
                        step = 0;
                        start = parseInt(res[1]);
                    } else {
                        if (res[2] == "-") res[2] = "-1";
                        step = res[2] ? parseInt(res[2]) : 1;
                        start = res[3] ? parseInt(res[3]) : 0;
                    }
                }
            }
            if (start < 1) {
                if (step < 1) {
                    step = null; //标志false
                } else {
                    start = -(-start) % step + step;
                }
            }
            return nthCache.set(param, {
                start: start,
                step: step
            });
        };
// ### parse Rule 相关
// 了解bison等解析器生成的同学可以把这部分看成是词法与语法定义的杂糅
// 很混乱也很不标准，但对于选择器这种最简单的DSL其实够用，并且有了奇效
// 整个Parser根据rules动态产生(即可在使用时发生改变)
// 具体的流程是下面的rules对象定义了一组语法(词法?)rule——如attribute，
// 你可以把每个rule中的reg想象成一个token(word?),这些token可能会有{{word}}这种占位符
// 占位符首先会被macros中对应的macro替换，然后这些token会被组装成一个大版的Regexp，即上面的
// Trunk变量,这个过程没什么特殊，一般比较优秀的选择器都是基于这个方法。 在nes中,最终的Trunk可能是
// 这样的:
//
// `/(\s*,\s*)|(#([\w\u4e00-\u9fbf-]+))|(\*|\w+)|(\.([\w\u4e00-\u9fbf-]+))|
// (:([\w\u4e00-\u9fbf-]+)(?:\(([^\(\)]*|(?:\([^\)]+\)|[^\(\)]*)+)\))?)|
// (\[([\w\u4e00-\u9fbf-]+)(?:([*^$|~!]?=)['"]?((?:[\w\u4e00-\u9fbf-]||\s)+)['"]?)?\])|(::([\w\u4e00-\u9fbf-]+))
// |([>\s+~&%](?!=))|(\s*\{\s*(\d*),(\-?\d*)\s*\}\s*)/g`
//
// 看到上面那长串，你大概理解了将regexp按词法分开这样做的第一个原因 : __维护__.
// 第二个原因就是: __效率__  一次大型正则的调用时间要远低于多次小型正则的匹配(前提它们做同样规模的匹配)
    var
// 一些macro
        macros = {
            split: "\\s*,\\s*",
// 分隔符
            operator: "[*^$|~!]?=",
// 属性操作符 如= 、!=
            combo: "[>\\s+~](?!=)",
// 连接符 如 > ~
            word: "[\\\\\\w\\u00A1-\\uFFFF-]"
        },
// 语法规则定义
        rules = {
            split: {
// 分隔符 如 ，
                reg: "{{split}}",
                action: function(all) {
                    this.parsed.push([null]);
                },
                order: 0
            },
// id 如 #home
            id: {
                reg: "#({{word}}+)",
                action: function(all, id) {
                    this.current().id = id;
                }
            },
// 节点类型选择符 如 div
            tag: {
                reg: "\\*|[a-zA-Z-]\\w*",
// 单纯的添加到
                action: function(tag) {
                    this.current().tag = tag.toLowerCase();
                }
            },
// 类选择符 如 .m-home
            classList: {
                reg: "\\.({{word}}+)",
                action: function(all, className) {
                    var current = this.current(),
                        classList = current.classList || (current.classList = []);
                    classList.push(className);
                }
            },
// 伪类选择符 如 :nth-child(3n+4)
            pesudos: {
                reg: ":({{word}}+)" + //伪类名
                "(?:\\(" + //括号开始
                "([^\\(\\)]*" + //第一种无括号
                "|(?:" + //有括号(即伪类中仍有伪类并且是带括号的)
                "\\([^\\)]+\\)" + //括号部分
                "|[^\\(\\)]*" + ")+)" + //关闭有括号
                "\\))?",
// 关闭最外圈括号
                action: function(all, name, param) {
                    var current = this.current(),
                        pesudos = current.pesudos || (current.pesudos = []),
                        name = name.toLowerCase(),
                        res = {
                            name: name
                        };
                    if (param) param = param.trim();
                    if (posPesudoReg.test(name)) {
// parse 的成本是很小的 尽量在find前把信息准备好
// 这里我们会把nth-child(an+b) 的 a 与 b 在不同输入下标准化
                        param = extractNthValue(param);
                    }
                    if (param) res.param = param;
                    pesudos.push(res);
                }
            },
// 属性选择符  如  [class=hahaha]
//
// 这里以属性选择符为例，说明下reg与action的关系
//
            attributes: {
                reg: "\\[\\s*({{word}}+)(?:({{operator}})[\'\"]?([^\'\"\\[]+)[\'\"]?)?\\s*\\]",
                action: function(all, key, operator, value) {
                    var current = this.current(),
                        attributes = current.attributes || (current.attributes = []);
                    var res = {};
                    attributes.push({
                        key: key,
                        operator: operator,
                        value: value
                    });
                }
            },
// 伪元素可以实现么？ 占位
            combo: {
                reg: "\\s*({{combo}})\\s*",
                action: function(all, combo) {
                    var data = this.parsed,
                        cur = data[data.length - 1];
                    this.current().combo = combo;
                    cur.push(null);
                },
                order: 0
            }
        };
    var cleanReg = new RegExp("\\s*(,|" + macros.combo + "|" + macros.operator + ")\\s*", "g");
    clean = function(sl) {
        return sl.trim().replace(/\s+/g, " ").replace(cleanReg, "$1");
    };
// ### parser生成
// 初始化parser实例
    var parser = new Parser();
    parser.on(rules); //生成规则
// 为了兼容前面版本，仍然提供这个parse函数, 也为了与find想对应
    function parse(sl) {
        return parser.parse(sl);
    }
//   3. Finder
// ================
//   Util
// -------------------------
// 将nodelist转变为array
//  DOM related Util
// --------------------
    var root = doc.documentElement || doc;
    var attrMap = {
        'for': "htmlFor",
        "href": function(node) {
            return "href" in node ? node.getAttribute("href", 2) : node.getAttribute("href");
        },
        "type": function(node) {
            return "type" in node ? node.getAttribute("type") : node.type;
        }
    };
    var checkTagName = assert(function() {
        testNode.appendChild(doc.createComment(""));
// 有些版本的getElementsByTagName("*")会返回注释节点
        return !testNode.getElementsByTagName("*").length ||
// 低版本ie下input name 或者 id为length时 length返回异常
            typeof doc.getElementsByTagName("input").length !== "number";
    });
//form __sizzle__line200 判断getAttribute是否可信
    var checkAttributes = assert(function() {
        testNode.innerHTML = "<select></select>";
        var type = typeOf(testNode.lastChild.getAttribute("multiple"));
// IE8 returns a string for some attributes even when not present
        return type !== "boolean" && type !== "string";
    });
// 将nth类方法的判断部分统一抽离出来,
// 其中type代表是否是nth-type-of类型的判断,下面类似
    function checkNth(node, type) {
        return type? node.nodeName === type : node.nodeType === 1;
    }
// 获得父节点node的顺数第n(从1开始)个子节点
    function nthChild(node, type) {
        var node = node.firstChild;
        return (!node || checkNth(node, type)) ? node : nthNext(node, type);
    };
// 获得父节点node的倒数第n(从1开始)个子节点
    function nthLastChild(node,type) {
        var node = node.lastChild;
        return (!node || checkNth(node, type))? node:nthPrev(node, type);
    };
// 获得节点node的第n(从1开始)个前置兄弟节点
    function nthPrev(node, type) {
        while (node = node.previousSibling) {
            if (checkNth(node, type)) return node;
        }
        return node;
    };
// 获得节点node的倒数第n(从1开始)个前置兄弟节点
    function nthNext(node, type) {
        while (node = node.nextSibling) {
            if (checkNth(node, type)) return node;
        }
        return node;
    };
// 获得节点node的key属性的值, 修改自from sizzle...蛋疼啊各浏览器的属性获取
    function getAttribute(node, key) {
        var map = attrMap[key];
        if (map) return typeof map === "function" ? map(node) : node[map];
        if (checkAttributes) {
            return node.getAttribute(key);
        }
        var attrNode = node.getAttributeNode(key);
// 对于selected checked 当返回为bool值时  将其标准化为 selected = "selected"
// 方便后续处理
// 很多时候null可以作为标志位，nes中大部分特殊flag都用null标示
        return typeof node[key] === "boolean"
            ? node[key] ? key : null
            : (attrNode && attrNode.specified ?attrNode.value : null);
    };
// __数组去重__
    function distinct(array) {
        for (var i = array.length; i--;) {
            var n = array[i];
// 先排除 即 如果它是清白的 后面就没有等值元素
            array.splice(i, 1, null);
            if (~array.indexOf(n)) {
                array.splice(i, 1); //不清白
            } else {
                array.splice(i, 1, n); //不清白
            }
        }
        return array;
    }
// 从sizzle抄袭的 document sorter
// 将匹配元素集按文档顺序排列好 这很重要!
    var sortor = (doc.compareDocumentPosition) ?
        function(a, b) {
            if (!a.compareDocumentPosition || !b.compareDocumentPosition) return 0;
            return a.compareDocumentPosition(b) & 4 ? -1 : a === b ? 0 : 1;
        } : ('sourceIndex' in doc) ?
        function(a, b) {
            if (!a.sourceIndex || !b.sourceIndex) return 0;
            return a.sourceIndex - b.sourceIndex;
        } : function(a, b) {
        var i = 0,
            ap = [a],
            bp = [b],
            aup = a.parentNode,
            bup = b.parentNode,
            cur = aup;
        if (a === doc) {
            return -1;
        } else if (b === doc) {
            return 1;
        } else if (!aup && !bup) {
            return 0;
        } else if (!bup) {
            return -1;
        } else if (!aup) {
            return 1;
        } else if (aup === bup) {
            return siblingCheck(a, b);
        }
        while (cur) {
            ap.unshift(cur);
            cur = cur.parentNode;
        }
        cur = bup;
        while (cur) {
            bp.unshift(cur);
            cur = cur.parentNode;
        }
        while (ap[i] === bp[i]) {
            i++;
        }
        return siblingCheck(ap[i], bp[i]);
    };
    function siblingCheck(a, b) {
        if (a && b) {
            var cur = a.nextSibling;
            while (cur) {
                if (cur === b) {
                    return -1;
                }
                cur = cur.nextSibling;
            }
        }
        return a ? 1 : -1;
    };
    function uniqueSort(nodeList) {
        return distinct(nodeList.sort(sortor));
    };
// ### nth position Cache 部分
// 对于nth类型的查找，有时候一次节点查找会遍历到多次相同节点，
// 由于一次节点查找时，由于js的单线程，节点不可能发生改变，介于此，我们将
// nth类的node的节点位置缓存起来，在本次查找结束后再清空
// 获得node的唯一标示
    var getUid = (function(token) {
        var _uid = 0;
        return function(node) {
            return node._uid || (node._uid = token + _uid++);
        };
    })("nes_" + (+new Date).toString(36));
// 创建nth相关的Filter，由于都类似，就统一通过工厂函数生成了
// 参数有两个
//    1. isNext: 代表遍历顺序是向前还是向后
//    2. isType: 代表是否是要指定nodeName
    function createNthFilter(isNext, isType) {
        var next, prev, cacheKey, getStart;
        if (isNext) {
            cacheKey = isType ? "type" : "child";
// if(typeof isType === "function") cacheKey = "match"
            next = nthNext;
            prev = nthPrev;
            getStart = nthChild;
        } else {
// Fixed:!!! 这里cache是首次生成的cache被写死了，即使后面clear了也没有用,
// 即永远无法被释放
            cacheKey = "last" + (isType ? "type" : "child");
// if(typeof isType === "function") cacheKey = "last-match"
            prev = nthNext;
            next = nthPrev;
            getStart = nthLastChild;
        }
// 实际返回函数, param即pesudo的action定义的参数形如
// `{step:1, start:1}` 所有的类似even、odd或者其他形如n、-3n-11都会标准化
// 成这种形势
        return function(node, param) {
            var cache = nthPositionCache[cacheKey];
            if (node === root) return false; // 如果是html直接返回false 坑爹啊
            var _uid = getUid(node),
                parent = node.parentNode,
                traverse = param.step > 0 ? next : prev,
                step = param.step,
                start = param.start,
                type = isType && node.nodeName;
//Fixed
            if (step === null) return false; //means always false
            if (!cache[_uid]) {
                var startNode = getStart(parent, type),
                    index = 0;
                do {
                    cache[getUid(startNode)] = ++index;
                    nthPositionCache.length++;
                } while (startNode = next(startNode, type));
            }
            var position = cache[_uid];
            if (step === 0) return position === start;
            return ((position - start) / step >= 0) && ((position - start) % step === 0);
        };
    }
//
    var nthPositionCache = {length: 1 };
    function clearNthPositionCache() {
        if (nthPositionCache.length) {
            nthPositionCache = {
                child: {},
                lastchild: {},
                type: {},
                lasttype: {},
                length: 0
            };
        }
    }
// 初始化positioncache
    clearNthPositionCache();
// 这里的几个finders是第一轮获取目标节点集的依赖方法
// 我没有对byClassName做细致优化，比如用XPath的方式
// form sizzle line 147
    var finders = {
        byId: function(id) {
            var node = doc.getElementById(id);
            return node ? [node] : [];
        },
        byClassName: doc.getElementsByClassName ? function(classList, node) {
            classList = classList.join(" ");
            return toArray((node || doc).getElementsByClassName(classList));
        } : null,
        byTagName: checkTagName ? function(tagName, node) {
            var results = (node || doc).getElementsByTagName(tagName);
            return toArray(results);
        } : function(tagName, node) {
            var results = (node || doc).getElementsByTagName(tagName);
            var elem, tmp = [],
                i = 0;
            for (;
                (elem = results[i]); i++) {
                if (elem.nodeType === 1) tmp.push(elem);
            }
            return tmp;
        }
    };
// ### filter:
// Action中塞入的数据会统一先这里处理，可能是直接处理如id、class等简单的.
// 也可能是分发处理，甚至是多重的分发，如那些复杂的attribute或者是pesudo
// 这里简化到过滤单个节点 逻辑清晰 ,但可能性能会降低，因为有些属性会重复获取
    var filters = {
        id: function(node, id) {
            return node.id === id;
        },
        classList: function(node, classList) {
            var len = classList.length,
                className = " " + node.className + " ";
            for (; len--;) {
                if (className.indexOf(" " + classList[len] + " ") === -1) {
                    return false;
                }
            }
            return true;
        },
        tag: function(node, tag) {
            if (tag == "*") return true;
            return node.tagName.toLowerCase() === tag;
        },
// pesudos会分发到ExpandsFilter中pesudo中去处理
        pesudos: function(node, pesudos) {
            var len = pesudos.length,
                pesudoFilters = expandFilters["pesudos"];
            for (; len--;) {
                var pesudo = pesudos[len],
                    name = pesudo.name,
                    filter = pesudoFilters[name];
                if (!filter) throw Error("不支持的伪类:" + name);
                if (!filter(node, pesudo.param)) return false;
            }
            return true;
        },
// attributes会分发到ExpandsFilter中的operator去处理
        attributes: function(node, attributes) {
            var len = attributes.length,
                operatorFilters = expandFilters["operators"];
            for (; len--;) {
                var attribute = attributes[len],
                    operator = attribute["operator"],
                    filter = operatorFilters[operator],
                    nodeValue = getAttribute(node, attribute.key);
                if (nodeValue === null) {
                    if (operator !== "!=") return false;
                    continue;
                }
                if (!operator) continue;
                if (!filter) throw Error("不支持的操作符:" + operator);
                if (!filter(attribute.value, nodeValue + "")) return false;
            }
            return true;
        }
    };
// expandFilters
// -------------------------
// 原生可扩展的方法
    var expandFilters = {
// __扩展连接符__:
// 选择符filter 与其他filter不同 node 同样是当前节点 区别是
// 如果成功返回成功的上游节点(可能是父节点 可能是兄弟节点等等)
// 其中 match(node) 返回 这个上游节点是否匹配剩余选择符(内部仍是一个递归)
        combos: {
            ">": function(node, match) {
                var parent = node.parentNode;
                if (match(parent)) return parent;
            },
            "~": function(node, match) {
                var prev = nthPrev(node);
                while (prev) {
                    if (match(prev)) return prev;
                    prev = nthPrev(prev);
                }
            },
            " ": function(node, match) {
                var parent = node.parentNode;
                while (parent) {
                    var pass = match(parent);
                    if (pass) return parent;
                    if (pass === null) return null;
                    parent = parent.parentNode;
                }
                return null;
            },
            "+": function(node, match) {
                var prev = nthPrev(node);
                if (prev && match(prev)) return prev;
            }
        },
// __扩展操作符__ :
        operators: {
            "^=": function(value, nodeValue) {
                if (nodeValue == null) return false;
                return nodeValue.indexOf(value) === 0;
            },
            "=": function(value, nodeValue) {
                return nodeValue === value;
            },
            "~=": function(value, nodeValue) {
                if (nodeValue == null) return false;
                return ~ (" " + nodeValue + " ").indexOf(value);
            },
            "$=": function(value, nodeValue) { //以value结尾
                return nodeValue.substr(nodeValue.length - value.length) === value;
            },
            "|=": function(value, nodeValue) { // 连接符
                return ~ ("-" + nodeValue + "-").indexOf("-" + value + "-");
            },
            "*=": function(value, nodeValue) { //出现在nodeValue的任意位置
                return ~ (nodeValue).indexOf(value);
            },
            "!=": function(value, nodeValue) {
                return nodeValue !== value;
            }
        },
// __扩展伪类__:
        pesudos: {
//TODO:这里如果出自 SELECtorAPI 标注下处处
            "not": function(node, sl) {
                return !matches(node, sl);
            },
            "matches": function(node, sl) {
                return matches(node, sl);
            },
// child pesudo 统一由工厂函数生成
            "nth-child": createNthFilter(true, false),
            "nth-last-child": createNthFilter(false, false),
            "nth-of-type": createNthFilter(true, true),
            "nth-last-of-type": createNthFilter(false, true),
            "first-child": function(node) {
                return !nthPrev(node);
            },
            "last-child": function(node) {
                return !nthNext(node);
            },
            "last-of-type": function(node) {
                return !nthNext(node, node.nodeName);
            },
            "first-of-type": function(node) {
                return !nthPrev(node, node.nodeName);
            },
            "only-child": function(node) {
                return !nthPrev(node) && !nthNext(node);
            },
            "only-of-type": function(node) {
                return !nthPrev(node, node.nodeName) && !nthNext(node, node.nodeName);
            },
//找出有具体text内容的节点
            "contains": function(node, param) {
                return ~ (node.innerText || node.textContent || '').indexOf(param);
            },
            "checked": function(node) {
                return !!node.checked || !! node.selected;
            },
            "selected": function(node) {
                return node.selected;
            },
            "enabled": function(node) {
                return node.disabled === false;
            },
            "disabled": function(node) {
                return node.disabled === true;
            },
            "empty": function(node) {
                var nodeType;
                node = node.firstChild;
                while (node) {
                    if (node.nodeName > "@" || (nodeType = node.nodeType) === 3 || nodeType === 4) {
                        return false;
                    }
                    node = node.nextSibling;
                }
                return true;
            },
            "focus": function(node) {
                return node === doc.activeElement && (!doc.hasFocus || doc.hasFocus()) && !! (node.type || node.href || ~node.tabIndex);
            },
            "target": function(node, param) {
                var id = node.id || node.name;
                if (!id) return false;
                return ("#" + id) === location.hash;
            }
        }
    };
// 这里主要是整合之前的ExpandsFilter中的mathch, 单层数据
    function matchDatum(node, datum, ignored) {
        var subFilter;
        for (var i in datum) {
            if (ignored !== i && (subFilter = filters[i]) && !subFilter(node, datum[i])) {
                return false;
            }
        }
        return true;
    };
// 这个全局cache的引入是为了避免多次传入参数。
// 当然全局的缺点也很明显，维护会不方便, 不利于测试
    var matchesCache = null; //保存那些matches函数
    function matchData(node, data, ignored) { // 稍后再看存入step
        var len = data.length,
            datum = data[len - 1];
// 首先要满足自身
        if (!matchDatum(node, datum, ignored)) return false;
        else {
            if (len == 1) return true;
            var nextDatum = data[len - 2],
                getNext = expandFilters.combos[nextDatum.combo],
                match = matchesCache[len - 2],
                next = getNext(node, match);
            if (next) return true;
            else return false;
        }
    };
//动态产生供FilterOneNode使用的match
    function createMatch(data) {
        return function(node) {
            if (node == root || node == null || node == doc) return null; //null 相当于休止符
            return matchData(node, data);
        };
    };
    function createMatches(data) {
        var matches = [];
        for (var i = 0, len = data.length; i < len; i++) {
            matches.push(createMatch(data.slice(0, i + 1)));
        }
        return matches;
    };
// 过滤主函数filter
// -----------------------------------
// 自底向上过滤非匹配节点
    function filter(results, data, ignored) {
        if (!data.length) return results;
//这里是为了缓存match匹配函数
        var preMatchesCache = matchesCache;
        matchesCache = createMatches(data);
        for (var i = results.length; i--;) {
            if (!matchData(results[i], data, ignored)) {
                results.splice(i, 1);
            }
        }
// Fixed: 因为一次filter可能会有字filter调用，比如matches、not、include
        matchesCache = preMatchesCache; // warning :以后写全局变量一定当心
        return results;
    }
// 获得第一次目标节点集
    function getTargets(data, context) {
        var results, ignored, lastPiece = data[data.length - 1];
        if (lastPiece.id) {
            results = finders.byId(lastPiece.id);
            ignored = "id";
        } else if (lastPiece.classList && lastPiece.classList.length && finders.byClassName) {
            results = finders.byClassName(lastPiece.classList, context);
            ignored = "classList";
        } else {
            results = finders.byTagName(lastPiece.tag || "*", context);
            ignored = "tag";
        }
        if (!results.length) return results;
        return filter(results, data, ignored);
    }
// API : find (private)
// -------------
// 根据parse后的数据进行节点查找
// options:
//    1. parsed.data  parse数据为一数组
//    2. node         context节点
// 事实上没有data这个单词，我这里算是自定了这个单词
//     datas : [data,data]
//     data : [datum, datum]
//     datum: {tag:"*"....etc}
    function find(datas, context) {
        if (!datas[0][0]) return [];
        var results = [],
            notNullResult = 0;
        for (var i = 0, len = datas.length; i < len; i++) {
            var data = datas[i],
                dlen = data.length,
                last = data[dlen - 1],
                result = getTargets(data, context);
            if (result && result.length) {notNullResult++;};
            if (!results) results = result;
            else results =results.concat(result);
        }
        clearNthPositionCache();//清理
        if (notNullResult > 1) uniqueSort(results);
        return results;
    }
// API : 测试用get相当于all (private)
// -------------------------------------
// 为了测试时避免原生querySelector的影响
//
    function get(sl, context) {
        var data = parse(sl);
        var result = find(data, context || doc);
        return result;
    }
// API
// ----------------------------------------------------------------------
    var supportQuerySelector = !! doc.querySelector;
// API1——__one__:对应标准的querySelector方法
    function one(sl, context) {
        var node;
        if (supportQuerySelector && !nes.debug) {
            try {
                node = (context || doc).querySelector(sl);
            } catch (e) {
                node = get(sl, context)[0];
            }
        } else {
            node = get(sl, context)[0];
        }
        return node;
    }
// API2——__all__
// -------------------------------
// 对应标准的querySelectorAll方法
    function all(sl, context) {
        var nodeList;
        if (supportQuerySelector && !nes.debug) {
            try {
                nodeList = toArray((context || doc).querySelectorAll(sl));
            } catch (e) {
                nodeList = get(sl, context);
            }
        } else {
            nodeList = get(sl, context);
        }
        return nodeList;
    }
// API 3:
// ----------------------------------------------------------------------
// 对应标准的matches方法
// nes的matches功能稍强，它支持用分隔符链接符组合的复杂选择器
// 即与all、one函数的支持是一样的
//
// 注: 由于:not与:matches依赖于这个函数 ,所以同样支持复杂选择器
    function matches(node, sl) {
        if (!node || node.nodeType !== 1) return false;
        var datas = parse(sl),
            len = datas.length;
        if (!datas[len - 1][0]) return false;
        for (; len--;) {
            if (matchOneData(node, datas[len])) return true;
        }
        return false;
    }
// matches 单步调用方法
    function matchOneData(node, data) {
        var len = data.length;
        if (!matchDatum(node, data[len - 1])) {
            return false;
        } else {
            return filter([node], data.slice(0)).length === 1;
        }
    }
// ASSEMBLE
// =========================
// 组装分为几个步骤
//
// 1. 生成pesudo 、 operator、combo 等expand方法
// ----------------------------------------------------------------------
// 具体扩展方法的使用请参见 [nes的github](https://github.com/leeluolee/nes)
// 统一由工厂函数createExpand
    ;
    (function createExpand(host, beforeAssign) {
        for (var i in host) {
            nes[i] = (function(i) {
                var container = host[i];
// autoSet代表了这三个函数除了key、value参数
// 也支持字面量的参数输入
                return autoSet(function(key, value) {
// Warning: 直接覆盖，如果存在的话
                    container[key] = value;
                    if (i in beforeAssign) {
                        beforeAssign[i](key, value);
                    }
                });
            })(i);
        }
// 有些扩展如combos、operators由于为了避免冲突
// 关键字都写入了正则式中，这种情况下需要将新的正则式
// 填入相关正则，并进行parser的setup
    })(expandFilters, {
        "operators": function(key) {
            var befores = macros.operator.split("]");
            befores.splice(1, 0, key.charAt(0) + "]");
            macros.operator = befores.join("");
            parser.setup();
        },
        "combos": function(key) {
            var befores = macros.combo.split("]");
            befores.splice(1, 0, key + "]");
            macros.combo = befores.join("");
            parser.setup();
        }
    });
// 2. 暴露API
// -------------------------------------
//
// 直接设置其为true 来强制不适用原生querySelector Api
    nes.debug = false;
    nes._nthCache = nthCache;
// parser , 抽离的parser部分
// ---------------------------
// 它可以:
//
//    1. parser.parse 解析内部规则定义的字符串匹配
//    2. parser.on    添加新规则
//    3. parser.clone 复制此parser，这个作用会在后面的zen-coding的demo中体现
//    4. parser.off   删除规则
//    5. parser.cache 缓存控制
    nes.parser = parser;
//解析, 这个将被移除，使用parser.parse来代替
    nes.parse = parse;
//查找parser解析后的data代表的节点 __private__
    nes._find = find;
//测试时排除原生querySelector的影响 __deprecated__! 使用nes.debug来控制
    nes._get = get;
//        *主要API*
// -------------------------
    nes.one = one;
    nes.all = all;
    nes.matches = matches;
// 内建扩展 api 这三个已经内建:
//
// 1. `pesudos`
// 2. `operators`
// 3. `combos`
    nes._uniqueSort = uniqueSort;
    nes._cleanSelector = clean;
    nes._getUid = getUid;
//          5.Exports
// ----------------------------------------------------------------------
// 暴露API:  amd || commonjs  || global
// 支持commonjs
    if (typeof exports === 'object') {
        module.exports = nes;
// 支持amd
    } else if (typeof define === 'function' && define.amd) {
        /* */define(function() {
            return nes;
        });
    } else {
// 直接暴露到全局
        win.nes = nes;
    }
//        6. extension
//-------------------------------------------------------------
// 很多人不看extend文件夹， 所以这部分也作为Demo实例
    /**
     * nth Math 的调用方法
     * @param  {[type]} first [description]
     * @return {[type]}
     */
    function nthMatch(first) {
        return function(node, param) {
            var tmp = param.split(/\s+of\s+/);
            if(tmp.length<2) throw Error("no 'of' keyword in nth-match\"s selector");
            var params = extractNthValue(tmp[0]),
                sl = tmp[1],
                testNode = node.parentNode[first? "firstChild":"lastChild"],
                next = first? "nextSibling" : "previousSibling",
                step = params.step,
                start = params.start,
                position = 0;
            if(!matches(node, sl)) return false;
            if (step === null) return false; //means always false
            do {
                if (testNode.nodeType === 1 && nes.matches(testNode, sl)) position++;
                if (testNode === node) break;
            } while (testNode = testNode[next]);
            if (step === 0) return position === start;
            return ((position - start) / step >= 0) && ((position - start) % step === 0);
        };
    }
    nes.pesudos({
// 例如 :nth-match(3 of li.active) 第三个满足这个li.active的节点
        "nth-match": nthMatch(true),
        "nth-last-match": nthMatch(false),
        "local-link": function(_node, param){
            if(param) param = parseInt(param);
        }
    });
}(window, document, undefined);
I$(28,function (NEJ,_t0,_p,_o,_f,_r){
    /**
     * 节点选择器
     *
     * 结构示例
     * ```html
     * <ul class="w-tab">
     *   <li class="itm">Tab-0</li>
     *   <li class="itm">Tab-1</li>
     *   <li class="itm">Tab-2</li>
     *   <li class="itm js-selected">Tab-3</li>
     *   <li class="itm">Tab-4</li>
     *   <li class="itm">Tab-5</li>
     * </ul>
     * ```
     *
     * 脚本示例
     * ```javascript
     * NEJ.define([
     *     'util/query/query',
     *     'util/tab/tab'
     * ],function(_e,_t){
*     // 使用选择器接口来取列表
*     _t._$$Tab._$allocate({
*         list:_e._$all('.w-tab > li'),
*         onchange:function(_event){
*                // TODO
*         }
*     });
* });
     * ```
     *
     * @method module:util/query/query._$all
     * @param  {String} arg0 - 选择器
     * @param  {Node}   arg1 - 用于匹配的根节点，默认为document
     * @return {Array}         符合规则的节点列表
     */
    _p._$all = function(){
        try{
            return nes.all.apply(nes,arguments);
        }catch(e){
            return null;
        }
    };
    /**
     * 节点选择器
     *
     * 结构示例
     * ```html
     * <ul class="w-tab">
     *   <li class="itm">Tab-0</li>
     *   <li class="itm">Tab-1</li>
     *   <li class="itm">Tab-2</li>
     *   <li class="itm js-selected">Tab-3</li>
     *   <li class="itm">Tab-4</li>
     *   <li class="itm">Tab-5</li>
     * </ul>
     * ```
     *
     * 脚本示例
     * ```javascript
     * NEJ.define([
     *     'util/query/query'
     * ],function(_t){
*     // 使用选择器接口来取选中的节点
*     var _node = _t._$one('.w-tab > li.js-selected');
* });
     * ```
     *
     * @method module:util/query/query._$one
     * @param  {String} arg0 - 选择器
     * @param  {Node}   arg1 - 用于匹配的根节点，默认为document
     * @return {Node}          符合规则的节点
     */
    _p._$one = function(){
        try{
            return nes.one.apply(nes,arguments);
        }catch(e){
            return null;
        }
    };
// for test only
    _p._$g = nes._get;
    if (CMPT){
        NEJ.copy(NEJ.P('nej.e'),_p);
    }
    return _p;
},14,29);
I$(27,function (_v,_e,_u,_x,_t){
    var fragmentRE = /^\s*<(\w+|!)[^>]*>/,
// local vals
        _slice = [].slice,
        _doc = document,
        _de = "documentElement",
        _docElem = _doc[_de],
        _testNode = _doc.createElement('div'),
// assert
        _textHandle = _testNode.textContent == null? 'innerText' : 'textContent' ,
        _extend = function(_name, _value, _options) {
            _options = _options || {};
            if (this[_name] == null || _options.override) this[_name] = _value;
            return this;
        },
        _bubbleUp = function(_sl, _node, _container) {
            while (_node && _node !== _container) {
                if (nes.matches(_node, _sl)){
                    return _node;
                }
                _node = _node.parentNode;
            }
        },
        /**
         * 根据返回类型决定返回this，还是别的什么
         * @param  {Mix} _result
         * @param  {String} _methodName 当前方法名
         * @return {Mix}
         */
        _ischainableRet = function(_result, _methodName, _node){
            return (_result === _node || _result === "undefined" || _result === this ||
            _result === _e || _result === _v);// 这两个是为了兼容nej
        },
        _isAcceptedNode = function(_node){
            if(!_node) return false;
            var _type = _node.nodeType;
            return _type === 1 || _type === 9 || //  element document
                _type === 11|| _node.window === _node; // framement window
        },
// 安全的添加原型, 本作用域内
        _safeProtoExtend = function(Type){
            var _proto = Type.prototype,
                _list = {};
            return {
                extend:function(_name, _fn){
                    _list[_name] = _proto[_name];//先保存之前的
                    _proto[_name] = _fn;
                    return this;
                },
                reset: function(){
                    for(var _i in _list) if(_list.hasOwnProperty(_i)){
                        if(_list[_i] === undefined){
                            delete _proto[_i];
                        }else{
                            _proto[_i] = _list[_i];
                        }
                    }
                }
            };
        },
        _fn = _safeProtoExtend(Function);
// 安全扩展函数原型
// 1. autoSet, 自动转换set({name:value})为多重set(name, value)
    _fn.extend("autoSet", function(){
        var _fn = this;
        return function(_key, _value) {
            if (_u._$isObject(_key)){
                var _args = _slice.call(arguments, 1);
                for(var _i in _key){
                    _fn.apply(this, [_i, _key[_i]].concat(_args));
                }
                return this;
            }else{
                return _fn.apply(this, arguments);
            }
        };
// 2. splitProcess, 自动在首参数为数组时，拆分为多步，
    }).extend("splitProcess", function(_isGetter){
        var _fn = this;
        return function(_params){
            if(_u._$isArray(_params)){
                var _args = _slice.call(arguments, 1),
                    _len = _params.length,
                    _ret;
                if(_isGetter) _ret = {}; //当时getter函数需要返回值
                for(var _i = 0 ; _i < _len ;_i++){
                    var _param = _params[_i],
                        _tmpRet = _fn.apply(this, [_param].concat(_args));
                    if(_isGetter && typeof _param === "string") _ret[_param] = _tmpRet;
                }
                return _isGetter? _ret : this;
            }else{
                return _fn.apply(this, arguments);
            }
        };
    });
    _extend = _extend.autoSet();
    /**
     *    将输入的选择器指定节点或节点和节点数组包装成_$$NodeList对象，NodeList是一个类似jQuery的对象
     *    可以进行链式操作，拥有大��分nej.e下的接口，并扩展了一部分jQuery的常用方法。
     *
     *    一个脑残的例子告诉你链式调用可以做什么
     *    ```javascript
     *    // 获得某个节点集, 设置样式
     *    $("#chainable li:nth-child(odd)")._$style({
*        "background": "#cca",
*        "cursor": "pointer"
*    })
     *    // 然后抛弃他们 找他们的下一个位置条件满足是4倍数的兄弟节点并设置样式
     *    ._$next(":nth-child(2n)")._$style({
*        "background": "#a19",
*        "cursor": "help"
*    })
     *    // 过滤出其中是4倍数的行,并绑定事件
     *    ._$filter(":nth-child(4n)")._$click(function(_e) {
*        $(this)._$style("background", "#111");
*    // 并给他们中的第一行设置边框
*    })._$get(1, true)._$style("border", "3px solid #222")
     *    // 找到父节点div并且有chainable的id并且设置样式
     *    ._$parent("div#chainable")._$style({
*        width: "800px",
*        left: "300px",
*        position:"absolute"
*    // 绑定事件以及代理事件
*    })._$on({
*        "click" :function(){
*            var div = document.createElement("div")
*            div.innerHTML = "haha插入一行"
*            //每次点击插入一行
*            $(this)._$insert(div, "bottom");
*        },
*        "mouseover li:nth-child(odd)":function(_e){
*            this._isLight = !this._isLight;
*            // 每次点击改变背景色
*            $(this)._$style("background-color", this._isLight? "#cca":"#331")
*        }
*    // 获得样式值
*    })._$style(["width", "left"])
     *    // 到这里链式结束返回{"width":"80px", "left":"30px"}
     *    ```
     *
     *    nej.$ 支持的选择器与nes选择器一致，具体请参考 https://github.com/leeluolee/nes
     *
     *    结构举例
     *    ```html
     *      <ul>
     *          <li><a href=""></a></li>
     *          <li><a href=""></a></li>
     *          <li><a href=""></a></li>
     *          <li><a href=""></a></li>
     *      </ul>
     *    ```
     *
     *    ```javascript
     *      var $ = NEJ.P('nej.$');
     *      $('ul > li:nth-child(2n+1) >a')
     *       .addClassName('odd')
     *       ._$on('click', _callback) //将所有的奇数li节点下的a标签加上className，并进行事件绑定
     *    ```
     *
     *    $接受的参数与jQuery的一致 ，非常灵活
     *    ```javascript
     *    // 获得"body"节点， 很明显此时节点集只有一个元素
     *    $("body")
     *
     *    // 找到有class1并且有rel属性的节点集，这时可能会有很多个节点
     *    $("body li.class1[rel]")
     *    // 会过滤出childNodes的节点，其他Array Like也是类似
     *    $(document.body.childNodes)
     *
     *    // 有时候你不确定输入的是什么参数， 安全的再包一次吧，无副作用
     *    $body = $("body")
     *    $body2 = $($body2)
     *    ```
     *
     *    @method CHAINABLE.$
     *    @param  {String|Array|_$$NodeList|Node} _selector 可以是选择器、节点、节点数组或另一个_$$NodeList实例
     *    @param  {String|Node|_$$NodeList} _context  代表从这个根节点下查找节点，特别是页面上节点还不存在时，需要传入这个参数
     *    @return {_$$NodeList}           返回_$$NodeList实例
     */
    var $ = function(_selector, _context){
// dump nej methods implement
        $._$implement(_x._$dump(), {"statics": true});
        _x._$clear();
        if (typeof _selector === 'string' && _selector.trim().indexOf("<") == 0) {
            var container = document.createElement('div');
            container.innerHTML = _selector;
            var res = $(container.childNodes);
            return res;
        }
        return new _$$NodeList(_selector, _context);
    };
    function _$$NodeList(_selector, _context){
        this.length = 0;
        this._signs = {};//标示是否有了当前节点
        this._context = _context || _doc;
        if(!_selector) return ;
        if(typeof _selector === "string"){
// if(/\^<[-\w]+/.test(_selector)) return $.fragment(_selector);
            if(_context && _context instanceof _$$NodeList) _context = _context[0];
            if(typeof _context == 'string') _context = $(_context)[0];
            this._$add(_t._$all(_selector, _context));
        }else if(_selector instanceof _$$NodeList || _isAcceptedNode(_selector) ||
            _selector.length){ // _$$NodeList 或者 是单节点、或者是类数组(如childNodes)
            this._$add(_selector);
        }
    }
// 扩展接口
    $._$extend = _extend._$bind($);
    $._$extend({
        _$signal: "_uid",//会绑定在节点上的唯一标示
        _$instances:{},// 缓存对象
        _$handlers:[], // 保存原始handler方法
        _$fragment: function(){
        },
        /**
         * 扩展链式化接口，你可以通过两种方式，一是迁移已有的静态接口(比如NEJ的大部分接口都是这样迁移过来的)，而是直接进行_$$NodeList的原型扩展
         *
         * Example:
         * ```javascript
         * // 1. 直接扩展
         * $._$implement("_$hello", function(){
*     // 遍历容器内的所有节点
*     this._$forEach(function(_node, _index){
*         _node.hello = "Hello World"
*     })
* })
         * $("li:nth-child(2n)")._$hello() // 所有偶数行都被加上了 hello属性
         * // 2. 直接利用静态方法进行扩展(常用语迁移), 上面扩展等价于
         * $._$implement("_$hello", function(_node){
*    _node.hello = "Hello World"
* }, {static: true})
         * // 3. 创建jQuey的wrap 方法
         * // 创建wrap方法
         * $._$implement("_$wrap", function(_selector){
*     var $content = $(_selector)
*     $content._$after2(this)._$insert(this);
* })
         * $("#list")._$wrap(document.createElement("div"))
         * ```
         *
         * 需要注意的是，当静态接口的迁移时，有如下约定(同时也是NEJ原接口在链式调用的表现约定)
         *
         * * 当返回值为: this 、 传入节点 、 nej.v 、 nej.e 、 undefined (即不返回)时, 视为setter操作,可以进行链式调用, 如上例:
         * * 当返回值为其他类型时: 视为getter操作, 返回节点列表中 第一个元素 的返回值，这个也是jQuery的链式接口的表现
         *
         *
         * @method CHAINABLE._$implement
         * @param  {Object} _definition 要扩展的接口集合 (注意不要使用字符串作为键值)
         * @param  {Object} _options 参数  目前只有两个选项{statics: 代表是否是静态接口迁移, override: 是否覆盖原同名方法}
         * @return {this}
         */
        _$implement: function(_name, _fn, _options){
            _options = _options || {};
            _extend.call(_$$NodeList.prototype, _name, _options.statics? this._transport(_fn): _fn);
        }.autoSet(),
        _transport: function(_fn){
            return function(){
// if(!this.length) throw Error("内部节点集为空")
                var _args = _slice.call(arguments);
                _args.unshift(this[0]);
                var _ret = _fn.apply(this,_args);
// 当返回_e、_v、this、_node、undefined(无返回值)都视为链式
                if(!_ischainableRet.call(this, _ret)) return _ret;
                this._$forEach(function(_node, _index){
                    if(_index === 0) return;
                    _args[0] = _node;
                    _fn.apply(this ,_args);
                });
                return this;
            };
        },
        _merge: function(_list1, _list2 , _filter){
            var _i = _list1.length || 0,
                _j = 0;
            for( ;_list2[_j] !== undefined;){
                var _tmp = _list2[_j++];
                if(!_filter || _filter.call(_list1, _tmp)){
                    _list1[_i++] = _tmp;
                }
            }
            _list1.length = _i;
            return _list1;
        },
        _toArray: function(_list){
            return $._merge([], _list);
        },
// ** fork form jQuery **
        _contains: _docElem.contains ? function( _a, _b ) {
            return _a === _b || (_a.nodeType == 9? _a[_de]: _a).contains(_b);
        }: _docElem.compareDocumentPosition ?
            function( _a, _b ) {
// more info : https://gist.github.com/4601579
                return _b && !!( _a.compareDocumentPosition( _b ) & 16 );
            }: function( _a, _b ) {
// fallback
            while ( (_b = _b.parentNode) ) {
                if ( _b === _a ) return true;
            }
            return false;
        },
        _$cloneNode:function(_node, _withContent){
            _withContent = !!_withContent;
            var _clone = _node.cloneNode(_withContent),
                _ce, _be;
            if(_withContent){
                _be = nes.all("*", _node);
                _be.push(_node);
                _ce = nes.all("*", _clone);
                _ce.push(_clone);
            }else{
                _be = [_node];
                _ce = [_clone];
            }
            for (_i = _ce.length; _i--;){
                _definitions.fixture.clone(_ce[_i], _be[_i]);
            }
            return _clone;
        },
        _delegateHandlers : {},// for delegate
        _cleanSelector : nes._cleanSelector,
        _$uniqueSort : nes._uniqueSort,
        _$matches : nes.matches,
        _$fn: _$$NodeList.prototype,
        _$uid : nes._getUid
    });
// proto function 扩展
// ================================
    var _rclickEvents = /^(?:click|dblclick|contextmenu|DOMMouseScroll|mouse(?:\w+))$/,
        _rkeyEvents = /^key(?:)/,
        _definitions ={
// for insert
// 这里统一视为_node2为插入点
            "insertor":{
                "top":function(_node, _node2){
                    _node.insertBefore(_node2, _node.firstChild);
                },
                "bottom": function(_node, _node2){
                    _node.appendChild(_node2);
                },
                "before":function(_node, _node2){
                    var _parent = _node.parentNode;
                    if(_parent) _parent.insertBefore(_node2, _node);
                },
                "after":function(_node, _node2){
                    var _parent = _node.parentNode;
                    if(_parent) _parent.insertBefore(_node2, _node.nextSibling);
                }
            },
            fixProps :{
// 确保表单元素属性被正确设置 IE lt9
                input: 'checked',
                option: 'selected',
                textarea: 'value',
// clone时 , IE某些版本不会正确设置text
                script:"text"
            },
            fixture:{
// dest src attribute fixed
                "clone": function(_dest, _src){
                    var _nodeName, _attr;
                    if (_dest.nodeType !== 1) {
                        return;
                    }
// lt ie9 才有
                    if (_dest.clearAttributes) {
                        _dest.clearAttributes();
                        _dest.mergeAttributes(_src);
                    }
// 判断是否有需要处理属性的节点
                    _nodeName = _dest.nodeName.toLowerCase();
                    if(_prop = _definitions.fixProps[_nodeName]){
                        _dest[_prop] = _src[_prop];
                    }
//移除节点标示
                    _dest.removeAttribute($._$signal);
// 移除ID:  TODO? 是否允许有重复ID?
                    _dest.removeAttribute("id");
                },
//patch event
                "event":function(_e){
                    var _type = _e.type;
                    var _button = _e.button;
                    _e.__fixed = true; //标示被fix过
                    _e.target = _e.target || _e.srcElement || document; //for ie
                    _e.metaKey = !!_e.metaKey; //低版本ie会返回undefined 应该返回
                    if(_e.target.nodeType === 3) _e.target = _e.target.parentNode;
                    if(_rclickEvents.test(_type)){ //如果是鼠标事件 则初始化page相关
                        _e.pageX = _v._$pageX(_e);
                        _e.pageY = _v._$pageY(_e);
                        if (_type === 'mouseover' || _type === 'mouseout'){//如果是鼠标事件中的mouseover与mouseout
                            var related = _e.relatedTarget || _e[(_type == 'mouseover' ? 'from' : 'to') + 'Element'];
                            while (related && related.nodeType == 3) related = related.parentNode;
                            _e.relatedTarget = related;
                        }
                    }
                    _e.which = _e.charCode != null ? _e.charCode : _e.keyCode;
                    if( !_e.which && _button !== undefined){
// http://api.jquery.com/event.which/ use which
                        _e.which = ( _button & 1 ? 1 : ( _button & 2 ? 3 : ( _button & 4 ? 2 : 0 ) ) );
                    }
                    if(!_e.preventDefault) _e.preventDefault = function(){
                        this.returnValue = false;
                        return this;
                    };
                    if(!_e.stopPropagation) _e.stopPropagation = function(){
                        this.cancelBubble = true;
                        return this;
                    };
                }
            }
        },
// for traverse
        _traverse = function(_direct){
            var _$matches = $._$matches;
            return function(_selector, _all){
                var _ret = $([]);
                if(typeof _selector === "boolean"){
                    _all = _selector;
                    _selector = null;
                }
                this._$forEach(function(_node){
                    var _tmp = _node[_direct];
                    while (_tmp) {
                        if(_tmp.nodeType ===1 && (!_selector || _$matches(_tmp, _selector))){
                            _ret._$add(_tmp);
                            if(!_all) break;
                        }
                        _tmp = _tmp[_direct];
                    }
                });
                return _ret;
            };
        };
    $._$implement({
        /**
         * 获取节点样式或者设置节点样式, 这个接口的表现与jQuery的css方法一致, 根据参数不同有不同的表现
         * 比如:
         * ```javascript
         * $('li')._$style(name) //相当于_$getStyle 返回样式值
         * $('li')._$style([name1,name2...]) //相当于多重_$getStyle 返回一个Object(如{"height:20px, width:30px..."})
         * $('li')._$style(name, value) // 相当于setStyle 返回this
         * $('li')._$style(obj) //相当于多重版setStyle(即原_$style) 返回this
         * ```
         * @method CHAINABLE._$style
         * @param  {String|Object|Array} _key  可以是String(单取值或设置)，一个对象(多重赋值)，一个数组(多重取值)
         * @param  {String} _value 样式值
         * @return {_$$Nodelist|String|Object} setter操作返回_$$NodeList，单重取值返回String，多重取值返回样式属性为键的Object，表现与jQuery的css接口一致
         */
        _$style: function(_key, _value){
            if(!_key) throw Error("缺少css样式名");
            if(_value === undefined){
                return _e._$getStyle(this[0], _key);
            }
            return this._$forEach(function(_node){
                _e._$setStyle(_node, _key, _value);
            });
        }.splitProcess(true).autoSet(),
        /**
         * 获取节点属性或者设置节点属性, 这个接口的表现与jQuery的attr一致, 同_$style接口，根据参数不同有不同的表现
         * 比如:
         * ```javascript
         * $('li')._$attr(name): 相当于_$attr 返回属性值
         * $('li')._$attr([name1, name2]) 同style描述 返回{titile:"xxx",rel:"xxx", href:"xxx"}
         * $('li')._$attr(name, value): 相当于_$attr 返回this
         * $('li')._$attr(obj): 相当于多重版的_$attr 返回this
         * ```
         *
         * @method CHAINABLE._$attr
         * @param  {String|Object|Array} _key  可以是String(单取值或设置)，一个对象(多重赋值)，一个数组(多重取值)
         * @param  {String} _value 属性值
         * @return {_$$Nodelist|String|Object} setter操作返回_$$NodeList，单重取值返回String，多重取值返回样式属性为键的Object，表现与jQuery的css接口一致
         */
        _$attr: function(_key, _value){
            if(!_key) throw Error("缺少属性名");
            if(_value === undefined){
                return _e._$attr(this[0], _key);
            }
            return this._$forEach(function(_node){
                _e._$attr(_node, _key, _value);
            });
        }.splitProcess(true).autoSet(),
        /**
         * 类似于ES5的Array#forEach, 一个遍历函数, 即遍历_$$NodeList的所有节点集
         * 比如:
         * ```javascript
         * // 将1,4,7...class含有strong的li元素分别加上阶梯型的高度
         * $("li.strong:nth-child(3n+1)")._$forEach(function(_node, _index){
*     _node.style.height = "" + (_index+1)*10 + "px";
*     // 这里的this指向实例
* })
         * ```
         * 注意callback中传入的节点是裸节点，而不是包装后的_$$NodeList
         *
         * @method CHAINABLE._$forEach
         * @param  {Function} _fn 遍历回掉，接受两个参数，当前遍历到的节点和节点下标
         * @return {_$$NodeList}
         */
        _$forEach: function(_fn){
            _u._$forEach(this, _fn);
            return this;
        },
        /**
         * 类似于ES5的Array#filter, 一个过滤, 即过滤_$$NodeList的所有节点集并筛选符合的节点
         * 比如:
         * ```javascript
         * // 返回节点集中的匹配选择器.strong:nth-child(3n)的节点
         * $("li")._$filter(".strong:nth-child(3n)")
         * // 相当于  ===>
         * $("li")._$filter(function(_node){
*     return $(_node)._$matches(".strong:nth-child(3n)");
* });
         * ```
         * 注意callback中传入的节点是裸节点，而不是包装后的_$$NodeList
         *
         * @method CHAINABLE._$filter
         * @param  {Function|String} _fn 遍历函数，接受两个参数，当前遍历到的节点和节点下标。同时也接受一个Selector，筛选出节点集中满足选择器的节点
         * @return {_$$NodeList}
         */
        _$filter: function(_fn){
            var _ret = [],
                _isSelctor = typeof _fn === "string";
            this._$forEach(function(_node, _index){
                var _test = _isSelctor ? $._$matches(_node, _fn):_fn.call(this, _node, _index);
                if(_test) _ret.push(_node);
            });
            return $(_ret);
        },
        /**
         * 相当于ES5的Array#map, 当返回值全部是节点类型时，返回$NodeListchainable, 否则返回标准结果数组(此时chainable不能)
         *
         * example:
         * ```javascript
         * // 此时返回Array : ["li", "li", "li".........]
         * $("li")._$map(function(_node){
*     return _node.tagName.toLowerCase()
* });
         * // 此时返回 $NodeList: 即所有节点的下一个兄弟节点
         * $("li")._$map(function(_node){
*     return _node.nextSibling
* });
         * ```
         * 注意callback中传入的节点是裸节点，而不是包装后的_$$NodeList
         *
         * @method CHAINABLE._$map
         * @param  {Function} _fn 遍历callback，接受两个参数，当前遍历到的节点和节点下标
         * @return {_$$NodeList}
         */
        _$map:function(_fn){
            var _ret = [],
                _isNotAllNode = false;
            this._$forEach(function(_node, _index){
                var _res = _fn.call(this, _node, _index);
                if(!_isAcceptedNode(_res)) _isNotAllNode = true;
                _ret.push(_res);
            });
            return _isNotAllNode ? _ret : $([])._$add(_ret);
        },
        /**
         * NodeList中的节点是不保证按文档顺序的(如果是用选择器，则保证是有序的), 你可以手动排序
         *
         * @method CHAINABLE._$sort
         * @return {_$$NodeList}
         */
        _$sort:function(){
            var _array = this._$get();
            $._$uniqueSort(_array);
            return $(_array);
        },
        /**
         * 向内部节点集填入元素, 会处理好重复以及过滤的逻辑。这个也是$接口依赖的方法。
         * ```javascript
         * var $body = $("body")
         * $body._$add($("tbody")) //==> 添加tbody
         * $body._$add($("tbody")) //==> 什么都不会发生 因为重复了
         * $body._$add(document.body.childNodes) //==> 添加所有的body下的子节点,过滤掉不符合的
         * ```
         *
         * @method CHAINABLE._$add
         * @param  {Node|Array|_$$NodeList} _node 要添加的节点或节点集
         * @return {_$$NodeList}      返回this
         */
        _$add:function(_node){
            if(!_node) return;
// TODO: 把window 排除在外
            if(_node.tagName || typeof _node.length !== "number" || _node === window ) _node = [_node];
            $._merge(this, _node, function(_nodum){
                if(!_isAcceptedNode(_nodum)) return false;
                var _uid = $._$uid(_nodum);
                if(this._signs[_uid]){
                    return false;
                }else{
                    this._signs[_uid] = 1;
                    return true;
                }
            });
            return this;
        },
        _$get:function(_index, wrap){
            if(typeof _index !== "number") return $._toArray(this);
            return wrap ? $(this[_index]) : this[_index];
        },
        _$last: function(wrap){
            return wrap? $(this[this.length-1]) : this[this.length-1];
        },
        _$first: function(wrap){
            return wrap? $(this[0]) : this[0];
        },
        /**
         * 判断包装节点是否满足某个选择器，即Selector API的matches方法。如果节点集内不止一个节点，则只判断第一个节点
         * Exmaple:
         * ```javascript
         *  $("body tbody td:nth-child(4n)")._$matches("body tbody td:nth-child(2n)")
         *  //返回 true... 这个是当然的, 4倍数的节点当然满足偶数条件
         * ```
         *
         *
         * @method CHAINABLE._$matches
         * @param  {String} _selector 供测试的选择器
         * @return {Boolean}          是否通过测试
         */
        _$matches: function(_selector){
            return $._$matches(this[0],_selector);
        },
        /**
         * 查找 所有节点 的第一个(或所有)满足关系的 父节点 集, 并返回$NodeList
         *
         * Example:
         * ```javascript
         * $("tr")._$parent()
         * //=> ['tbody', 'thead'],两个是因为节点集中的tr元素可能在tbody或thead中
         * $("tr")._$parent("tbody")
         * //=> ['tbody'] 必须满足tbody
         * $("tr")._$parent(true)
         * // =>['tbody', 'thead', 'div', 'body' ....] //会向上查找所有父节点
         * $("tr")._$parent("tbody, body",true)
         * // =>['body', 'tbody'] //会向上查找所有父节点,但是必须满足选择器
         * ```
         * @method CHAINABLE._$parent
         * @param  {String} _selector 选择器
         * @param  {Boolean} _all     是否获取所有层级的父节点
         * @return {[type]}
         * @type {[type]}
         */
        _$parent: _traverse("parentNode"),
        /**
         * 与_$parent类似,查找 所有节点 的第一个(或所有根据_all参数)满足关系的 前序兄弟节点 (previousSibling)集, 并返回$NodeList
         * ```javascript
         * $("td")._$prev("th[scope=row]", true)
         * // 返回所有在td之前的th元素, 它们的scope属性为 row
         * $("td")._$prev("th[scope=row]")
         * // 只返回直接相邻的前节点，如果不满足选择器则返回空节点集
         * ```
         * @method CHAINABLE._$prev
         * @param  {String} _selector 选择器
         * @param  {Boolean} _all     是否获取所有前序节点
         * @return {[type]}
         */
        _$prev: _traverse("previousSibling"),
        /**
         * 与_$prev类似,查找 所有节点 的第一个(或所有根据_all参数)满足关系的 向后兄弟节点 (nextSibling)集, 并返回$NodeList
         * @method CHAINABLE._$next
         * @param  {String} _selector 选择器
         * @param  {Boolean} _all     是否获取所有后序节点
         * @return {[type]}
         */
        _$next: _traverse("nextSibling"),
        /**
         * 查找到 本节点集中 所有节点 的满足选择器关系的 直接子节点 (或 任意层级子节点 )集, 并返回$NodeList
         * ```javascript
         * $("body, table")._$children();
         * // => 相当于 合并body与table的直接子节点
         * $("body, table")._$children("div, thead");
         * // => 只要他们子节点中的div 与 thead元素
         * $("body, table")._$children(true);
         * // => 这里会获取所有body下的所有层级的子节点(table也在body中)
         * $("body, table")._$children("td:not(:last-child, :nth-child(2n))",true);
         * // => 返回所有层级的td元素并且满足选择器 td:not(:last-child, :nth-child(2n))
         * ```
         *
         * @method CHAINABLE._$children
         * @param  {String} _selector 选择器
         * @param  {Boolean} _all     是否获取所有层级的节点
         * @return {[type]}
         */
        _$children: function(_selector, _all){
            var _ret = $([]);
            if(typeof _selector === "boolean"){
                _all = _selector;
                _selector = null;
            }
            this._$forEach(function(_node){
                var _backed = _all? _t._$all(_selector || "*", _node)
                    : _selector? $(_node.childNodes)._$filter(_selector)
                    : $(_node.childNodes);
                _ret._$add(_backed);
            });
            return _ret;
        },
        /**
         * 满足选择器条件的同级节点，但不包含本身
         * Example
         * ```javascript
         * $("script")._$siblings("title,h2"); // => 返回script的同级节点中的
         * ```
         *
         *
         * @method CHAINABLE._$siblings
         * @param  {String} _selector
         * @return {_$$NodeList}    这些同级节点会被包装为一个_$$NodeList
         */
        _$siblings: function(_selector){ // sibling 默认就是取所有
            return this._$prev(_selector, true)._$add(this._$next(_selector, true));
        },
        /**
         * 这个insert 拥有jQuery的四个接口的功能(before, after, prepend , append) ，分别用_direct参数控制
         *
         * Example:
         * ```javascript
         * //将`a.next`插到`#home`的内部的最上方
         * $('#home')._$insert('a.next', 'up');
         * //将a.next插入到`#home`节点后面
         * $('#home')._$insert('a.next', 'after');
         * ```
         *
         * @method CHAINABLE._$insert
         * @param  {String|Node|_$$NodeList} _selector 代表被插入的节点，可以是选择器、节点或是另外一个_$$NodeList对象
         * @param  {String} _direct   插入位置，可以是节点内的底部、顶部(bottom, top)，或节点同层的前后位置(before, after)，默认为bottom
         * @return {_$$NodeList}    返回this
         */
        _$insert: function(_selector, _direct){
            _direct = (_direct && _direct.toLowerCase()) || "bottom";
            if(!_definitions.insertor[_direct]) _direct = "bottom";
            var _content = $(_selector)[0], //将被插入的节点
                _insertor = _definitions.insertor[_direct];
            if(!_content) throw Error("The Element to be inserted is not exist");
            return this._$forEach(function(_node, _index){
                _insertor(_node, _index === 0? _content
                    : $._$cloneNode(_content, true));//如果是多个节点则cloneNode
            });
        },
        /**
         * 这个_$insert2 拥有jQuery的四个接口的功能(insertBefore, insertAfter, prependTo , appendTo) ，分别用_direct参数控制。其实就是_$insert接口的相反版，
         * 你做的是将被插入节点插入到某个节点的指定位置。
         *
         * Example:
         * ```javascript
         * //将`#home`插到`a.next`的内部的最上方
         * $('#home')._$insert2('a.next', 'up');
         * //将`#home`插入到`a.next`节点后面
         * $('#home')._$insert2('a.next', 'after');
         * ```
         *
         * @method CHAINABLE._$insert2
         * @param  {String|Node|_$$NodeList} _selector 代表参考节点，可以是选择器、节点或是另外一个_$$NodeList对象
         * @param  {String} _direct   插入位置，可以是节点内的底部、顶部(bottom, top)，或节点同层的前后位置(before, after)，默认为bottom
         * @return {_$$NodeList}    返回this
         */
        _$insert2: function(_selector, _direct){
            $(_selector)._$insert(this, _direct);
            return this;
        },
        /**
         * 克隆节点集内部的 所有节点, 并返回clone的目标节点集 $NodeList 实例
         *
         * Example:
         * ```javascript
         * $('.m-template')._$clone(true)._$insert2('body');//将`.m-template`节点clone一份插入到`body`的内部下方
         * ```
         *
         * @method CHAINABLE._$clone
         * @param  {Boolean} _withContent 是否要克隆子节点
         * @return {_$$NodeList}
         */
        _$clone: function(_withContent){
            return this._$map(function(_node){
                return $._$cloneNode(_node, _withContent);
            });
        },
        /**
         * 获得节点集中的 第一个元素的innerText 或者 设置所有元��的innerText
         *
         * Example:
         * ```javascript
         * $("title,h2")._$text("haha")
         * // 同时设置title与h2的text内容为haha
         * $("title,h2")._$text()
         * // 获得title(第一个元素)的innerText
         * ```
         *
         *
         * @method CHAINABLE._$text
         * @param  {content} _content 要插入的内容 , 不传入则认为是getter操作
         * @return {_$$NodeList|String} setter操作返回_$$NodeList getter操作返回String
         */
        _$text: function(_content){
            if(_content === undefined){
                if(!this[0]) throw Error("内部节点为空，无法完成get操作");
                return this[0][_textHandle];
            }
            return this._$forEach(function(_node){
                _node[_textHandle] = _content;
            });
        },
        /**
         * 获得节点集中的 第一个元素的innerHTML 或者设置所有元素的innerHTML(与_$text接口类似)
         *
         * Example:
         * ```javascript
         * $("title,h2")._$html("haha")
         * // 同时设置title与h2的innerHTML为haha
         * $("title,h2")._$html()
         * // 获得title(第一个元素)的innerHTML
         * ```
         *
         *
         * @method CHAINABLE._$html
         * @param  {content} _content 要插入的内容 不传入则认为是getter操作
         * @return {_$$NodeList|String} setter操作返回_$$NodeList getter操作返回String
         */
        _$html: function(_content){
            if(_content === undefined){
                if(!this[0]) throw Error("内部节点为空，无法完成get操作");
                return this[0].innerHTML;
            }
            return this._$forEach(function(_node){
                _node.innerHTML = _content;
            });
            return this;
        },
        /**
         * 获得节点集中的 第一个元素的value 或者设置所有元素的value(与_$text接口类似)
         *
         * Example:
         * ```javascript
         * $("input,textarea")._$val()
         * // 获取第一个满足'input,textarea'选择器元素的value值
         * $("title,h2")._$html("haha")
         * // 获得title(第一个元素)的innerHTML
         * ```
         *
         *
         * @method CHAINABLE._$html
         * @param  {content} _content 要插入的内容
         * @return {_$$NodeList|String} setter操作返回_$$NodeList getter操作返回String
         */
        _$val:function(_content){
            if(_content === undefined){
                if(!this[0]) throw Error("内部节点为空，无法完成get操作");
                return this[0].value;
            }
            return this._$forEach(function(_node){
                _node.value = _content;
            });
            return this;
        },
// 事件相关
// ==============
// 私有方法  注册事件代理
        _delegate:function(_event, _selector, _handler){
            _selector = $._cleanSelector(_selector);
            return this._$forEach(function(_node){
                var _uid = $._$uid(_node),
                    _handlers = $._delegateHandlers[_uid] || ($._delegateHandlers[_uid] = {}),
                    _events = _handlers[_event] || (_handlers[_event] = {}),
                    _selectors = _events[_selector] || (_events[_selector] = []);
                var _realCb = function(_e) {//正式回调
                    var _trigger;
                    if (_trigger = _bubbleUp(_selector, _e.target || _e.srcElement , _node)) {
                        _handler.apply(_trigger, arguments);
                    }
                };
// 保存引用 以可以正确off
                _realCb._raw = _handler;
                _selectors.push(_realCb);
// 假如不存在对应的容器，则先创建
                _v._$addEvent(_node, _event, _realCb);
// Fix: 我们保存原始_handler为了 nej的 delEvent可以正确解绑
// 省去再存储一份handler列表的开销
            });
        },
// 私有方法 解绑事件代理
        _undelegate:function(_event, _selector, _handler){
            _selector = $._cleanSelector(_selector);
            return this._$forEach(function(_node){
                var _uid = $._$uid(_node);
                var _handlers, _events, _selectors;
                if (!(_handlers = $._delegateHandlers[_uid]) ||
                    !(_events = _handlers[_event]) || !(_selectors = _events[_selector])){
                    return;
                }
                for(var _len = _selectors.length;_len--;){
                    var _fn = _selectors[_len];
//如果没有传入_handler或者 函数匹配了
                    if(!_handler || _fn._raw === _handler){
                        _v._$delEvent(_node, _event, _fn);
                        _selectors.splice(_len,1);
                    }
                }
// 如果被删光了
                if(!_selectors.length) delete _events[_selector];
            });
            return this;
        },
        /**
         * 绑定事件，可以使用事件代理, 与jQuery的on类似
         *
         * __Example:__
         * ```javascript
         * // 1. 普通事件绑定
         * $("body")._$on("click", function(_e){
*     alert("单个事件绑定"+_e.type)
* })
         * // 2. 多个普通类型绑定到同���个handler
         * $("body")._$on(["click", "mouseover"], function(_e){
*     alert("多个type绑定"+_e.type)
* })
         * // 3. 单个代理事件绑定 这里等同于_$on("click", "tr:nth-child(2n)", handler)
         * $("body")._$on("click tr:nth-child(2n)", function(_e){
*     // this 对象指向当前`触发`事件的tr:nth-child(2n)
*     _e.preventDefault()
*     alert("单个代理事件绑定"+_e.type)
* })
         * // 4. 多个事件绑定(同回调), 这里分别是普通事件dblclick与代理事件click tr:nth-child(2n)
         * $("body")._$on(["dblclick", "click tr:nth-child(2n)"], function(_e){
*     _e.preventDefault()
*     alert("多个事件类型绑定"+_e.type)
* })
         * // 5. 多重事件绑定,
         * $("body")._$on({
*     "dblclick":function(_e){
*         alert("多重事件绑定之普通版"+_e.type)
*     },
*     "click tr:nth-child(2n)":function(_e){
*         alert("多重事件绑定之代理版"+_e.type)
*     }
* })
         * ```
         *
         * @method CHAINABLE._$on
         * @param  {String|Array|Object} _event     事件名，_event支持多种参数类型会有不同的结果
         *                             如果_event参数中不包含空格, 则视为简单事件绑定如，click,
         *                             如果_event参数中包含空格,则会被split, 左边视为event参数，右边视为_selector参数如'click .next',
         *                             如果_event是个Ojbect,则会视为多重绑定,如{'click .next': callback1, 'mouseover': callback2}
         *                             如果_event是个Array, 则会对多个_event进行同一个函数的绑定, 如['click','mouseover']
         * @param  {String} _selector  如果传入则代表是一个事件代理,可忽略
         * @param  {Function} _handler 回掉函数
         * @return {_$$NodeList}
         */
        _$on:function(_event, _selector, _handler){
            if(_event === undefined) throw Error("缺少事件名参数");
            if(typeof _selector === "function"){
                _handler = _selector;
                _selector = null;
            };
            var _index = _event.indexOf(" ");
            if(~_index){//有空格分隔 如"click div.m-model"
                _selector = _event.slice(_index + 1);
                _event = _event.slice(0, _index);
            }
            if(!_handler) throw Error("缺少回调函数");
// 创建一个realHandler
            else {
                var _raw = _handler;
                var _handler = function(_e){
                    _definitions.fixture.event(_e);
                    _raw.apply(this, arguments);
                };
                _raw.real = _handler;//
            }
            if(_selector){ // on ("click", "li.clas1", handler)或 on("click", "li.class1")
                return this._delegate(_event,_selector, _handler);
            }
// on("click", handler)
            return this._$forEach(function(_node){
                _v._$addEvent(_node, _event, _handler);
            });
        }.splitProcess().autoSet(),
        /**
         * 为 节点集内的每一个节点 解除事件回调, 类似jQuery的off方法
         * __Example__
         * ```javascript
         * // 1. 普通事件解绑
         * $("body")._$off("click", handler)
         * // 2. 多个普通类型事件解绑(同一个handler)
         * $("body")._$off(["click", "mouseover"], handler)
         * // 3. 普通事件清除(即不传入handler) __同时会把节点上click类型的代理事件清除!__
         * $("body")._$off("click")
         * // 4. 多个普通事件清除 同时会把节点上相应类型的代理事件清除!
         * $("body")._$off(["click","mouseover"])
         * // 5. 单个代理事件的解绑
         * $("body")._$off("click","tr:nth-child(2n)", handler)
         * // 或
         * $("body")._$off("click tr:nth-child(2n)", handler)
         * // 6. 多个代理事件的解绑(同一个handler)
         * $("body")._$off(["dblclick td[title]", "click tr:nth-child(2n)"], handler)
         * // 7. 代理事件的清除
         * $("body")._$off("dblclick","td[title]");
         * $("body")._$off("dblclick td[title]");
         * $("body")._$off(["dblclick td[title]", "click tr:nth-child(2n)"])
         * // 8. 多重事件解绑
         * $("body")._$off({
*     "dblclick td":handler1,
*     "click tr":handler2
* });
         * // 9. 所有事件清除
         * $("body")._$off() //慎重
         * ```
         *
         *
         * @method CHAINABLE._$off
         * @param  {String|Array|Object} _event 与_$on方法一样，解绑也会根���参数不同可以有很大的灵活度
         *                                      如果_event参数中不包含空格, 则视为简单事件解绑如，click,
         *                                      如果_event参数中包含空格,则会被split, 左边视为event参数，右边视为_selector参数如'click .next',
         *                                      如果_event是个Ojbect,则会视为多重解绑, 如{'click .next': callback1, 'mouseover': callback2}
         *                                      如果_event是个Array, 则会对多个_event进行同一个函数的解绑, 如['click','mouseover']
         *                                      需要注意_$off与_$on不同的是_event也可以是个空值，代表会解决节点下的所有事件
         * @param  {[type]} _selector [description] 如果传入_selector参数，则会进行事件代理的事件解绑, 可忽略
         * @param  {[type]} _handler  [description] 要解绑对应回调，可忽略
         * @return {_$$NodeList}
         */
        _$off:function(_event, _selector, _handler){
            if(typeof _selector === "function"){
                _handler = _selector;
                _selector = null;
            }
            var _index;
            if(_event && ~(_index = _event.indexOf(" "))){//有空格分隔 如"click hello"
                _selector = _event.slice(_index + 1);
                _event = _event.slice(0, _index);
            }
            if(_handler) _handler = _handler.real || _handler;
            if(_selector){ // off("click", ".class")   off("click", ".class", handler)
                return this._undelegate(_event, _selector, _handler);
            }
            return this._$forEach(function(_node){
                var _uid = $._$uid(_node),
                    _handlers = $._delegateHandlers[_uid],
                    _events;
                if(!_event){ // off()
                    if(_handlers){
                        delete $._delegateHandlers[_uid]; // 删除所有
                    }
                    _v._$clearEvent(_node, _event);
                }else{
                    if(_handlers) _events = _handlers[_event];
                    if(!_handler){ // off("click")
                        if(_events){
                            delete _handlers[_event];
                        }
                        _v._$clearEvent(_node, _event);
                    }else{ // off("click", handler)
// 这里不对delegate做清理是因为 这样不会对delegate发生影响
                        _v._$delEvent(_node, _event, _handler);
                    }
                }
            });
        }.splitProcess().autoSet(),
        /**
         * 触发每个节点的对应事件, 同nej.v._$dispatchEvent，区别是参数类型自由度高一点
         *                                      如果_event参数为String, 则视为简单事件触发如，click,
         *                                      如果_event是个Ojbect,则会视为多重触发, 如{'click': param1, 'mouseover': param2}
         *                                      如果_event是个Array, 则会对多个_event进行触发(公用一个options), 如['click','mouseover']
         * Example:
         * ```javascript
         * //触发一个事件
         * _$trigger("click", params)
         * //一次触发多个事件(如果有参数，他们共用这个参数)
         * _$trigger(["click", "mouseover"], params)
         * // 触发多个事件有不同参数
         * _$trigger({
*     "click": params1,
*     "dblclick": params2
* })
         * ```
         *
         * @method CHAINABLE._$trigger
         * @param  {String|Array|Object} _event   可以传入多种参数类型
         * @param  {Whatever} _options 同_$dispatchEvent的_options
         * @return {_$$NodeList}
         */
        _$trigger:function(_event, _options){
            if(typeof _event !== 'string') throw Error("事件类型参数错误");
            this._$forEach(function(_node){
                _v._$dispatchEvent(_node, _event, _options);
            });
            return this;
        }.splitProcess().autoSet(),
// http://stackoverflow.com/questions/6599071/array-like-objects-in-javascript
// 让这个对象看起来像数组
        splice: function(){ throw Error("don't use the NodeList#splice");}
    });
// @ remove 无法被混淆的方法
// // 无奈 添加 _$before // _$before2   _$bottom _$bottom2等方法
// _u._$forIn(_definitions.insertor, function(_value, _key){
//     $._$implement("_$" + _key, function(){
//        var _args = _slice.call(arguments);
//        _args.push(_key)
//        return this._$insert.apply(this, _args)
//     })
//     $._$implement("_$" + _key+"2", function(){
//        var _args = _slice.call(arguments);
//        _args.push(_key)
//        return this._$insert2.apply(this, _args)
//     })
// })
// // 添加类似 _$click的事件
// // ================================
// // TODO: 检查是否有遗漏的方法
//    @
// var _beAttached = "click dbclick blur change focus focusin focusout keydown keypress keyup mousedown mouseover mouseup mousemove mouseout scroll select submit".split(" ");
// @ remove 无法被混淆 移除
// _u._$forEach(_beAttached, function(_eventName){
//     $._$implement("_$"+_eventName, function(){
//         var _type = typeof arguments[0];
//         var _args = _slice.call(arguments);
//         _args.unshift(_eventName);
//         // click("li", handler)   或者  click(handler)
//         if((_type == "function") || (_type === "string" && typeof arguments[1] === "function")){
//             this._$on.apply(this, _args);
//         }else{
//         // click(options) 或者 click()
//             this._$trigger.apply(this, _args);
//         }
//         return this;
//     }.autoSet())
// });
// 把原型还回去, WARN:千万注意
    _fn.reset();
    if (CMPT){
        nej.$ = $;
    }
    return $;
},3,4,2,18,28);
I$(6,function (_l){
    return _l;
},27);
I$(30,function (NEJ,_k,_v,_u,_p,_o,_f,_r){
    var _pro;
    /**
     * 控件基类，主要实现以下功能：
     * * 对事件驱动编程模型的支持
     * * 对控件通用行为及业务逻辑的抽象
     *
     * ```javascript
     *   NEJ.define([
     *       'base/klass',
     *       'util/event'
     *   ],function(_k,_t,_p,_o,_f,_r){
*       // 自定义一个控件及使用、回收的流程
*       var _pro;
*
*       // 第一步
*       // 定义控件类，从父类继承
*       _p._$$Widget = _k._$klass();
*       _pro = _p._$$Widget._$extend(_t._$$EventTarget);
*
*       // 第二步
*       // 重写控件初始化业务逻辑
*       _pro.__init = function(_options){
*           // _options - 配置参数信息
*           //            初始化时一般不对该参数做处理
*           // 调用父类初始化业务逻辑
*           this.__super(_options);
*           // TODO something
*       };
*
*       // 第三步
*       // 重写控件重置业务逻辑
*       _pro.__reset = function(_options){
*           // _options - 配置参数信息
*           //            此处重置控件配置信息
*           // 调用父类重置业务逻辑
*           this.__super(_options);
*           // TODO something
*       };
*
*       // 第四步
*       // 重写控件回收业务逻辑
*       _pro.__destroy = function __destroy(){
*           // 调用父类回收业务逻辑
*           this.__super();
*           // TODO something
*       };
*
*       // 第五步
*       // 使用控件
*       var _widget = _p._$$Widget._$allocate({
*           a:'aaaaaaaaaaa',
*           b:'bbbbbbbbbbbbb',
*           c:'ccccccccccccccc'
*       });
*
*       // 第六步
*       // 回收控件
*       _widget = _widget._$recycle();
*       // 也可以使用以下方式回收，建议使用上面的回收方式
*       _widget = _p._$$Widget._$recycle(_widget);
*   });
     * ```
     *
     * @class module:util/event._$$EventTarget
     * @param {Object} config - 配置参数，根据控件实际情况提供配置参数支持
     */
    /**
     * 控件回收前触发事件，控件在具体实现时如需触发回收前的事件
     *
     * ```javascript
     *   // 重写控件回收业务逻辑触发onbeforerecycle事件
     *   _pro.__destroy = function(){
*       this._$dispatchEvent('onbeforerecycle');
*       // 调用父类回收业务逻辑
*       this.__super();
*       // TODO something
*   };
     *
     *   // 监测onbeforerecycle事件
     *   var _widget = _p._$$Widget._$allocate({
*       onbeforerecycle:function(_event){
*           // TODO something
*       }
*   });
     * ```
     *
     * @event module:util/event._$$EventTarget#onbeforerecycle
     * @param {Object} event - 事件触发信息
     */
    /**
     * 控件回收后触发事件，控件在具体实现时如需触发回收后的事件
     *
     * ```javascript
     *   // 重写控件回收业务逻辑触发onbeforerecycle事件
     *   _pro.__destroy = function(){
*       // 调用父类回收业务逻辑
*       this.__super();
*       // TODO something
*       this._$dispatchEvent('onaftercycle');
*   };
     *
     *   // 监测onaftercycle事件
     *   var _widget = _p._$$Widget._$allocate({
*       onaftercycle:function(_event){
*           // TODO something
*       }
*   });
     * ```
     *
     * @event module:util/event._$$EventTarget#onaftercycle
     * @param {Object} event - 事件触发信息
     */
    _p._$$EventTarget = _k._$klass();
    _pro = _p._$$EventTarget.prototype;
    /**
     * 控件分配，NEJ框架提供的所有控件统一使用分配和回收机制，
     * 分配空间时会优先考虑使用前面回收的同种控件，只有在没有可用控件的情况下才会实例化新的控件
     *
     * ```javascript
     *   // 分配一个控件
     *   var _widget = _p._$$Widget._$allocate({
*       conf0:'aaaaaaa',
*       conf1:'bbbbbbbbbbbbb',
*       onxxx:function(){
*           // TODO something
*       }
*   });
     * ```
     *
     * @method module:util/event._$$EventTarget._$allocate
     * @see    module:util/event._$$EventTarget._$getInstance
     * @see    module:util/event._$$EventTarget._$getInstanceWithReset
     * @param  {Object}  arg0 - 配置参数，根据控件实际情况提供配置参数支持
     * @return {module:util/event._$$EventTarget} 控件实例
     */
    _p._$$EventTarget._$allocate = function(_options){
        _options = _options||{};
        var _instance = !!this.__pool
            &&this.__pool.shift();
        if (!_instance){
            _instance = new this(_options);
            this.__inst__ = (this.__inst__||0)+1;
        }
// reset instance, flag first
        _instance.__reset(_options);
        return _instance;
    };
    /**
     * 控件回收，NEJ框架提供的所有控件统一使用分配和回收机制，
     * 如果提供的实例非当前类的实例则自动调整为输入实例的类来回收此实例
     *
     * ```javascript
     *   // 回收前面分配的实例有两种方式
     *   // 如果不能确定实例的构造类，则可以直接使用实例的回收接口
     *   _widget._$recycle();
     *   // 如果可以确定实例的构造类，则可以使用构造类的静态回收接口
     *   _p._$$Widget._$recycle(_widget);
     *   // 如果回收多个实例则使用构造类的静态回收接口
     *   _p._$$Widget._$recycle([_widget0,_widget1]);
     * ```
     *
     * @method module:util/event._$$EventTarget._$recycle
     * @param  {module:util/event._$$EventTarget|module:util/event._$$EventTarget[]} arg0 - 待回收实例或者实例列表
     * @return {Void}
     */
    _p._$$EventTarget._$recycle = (function(){
        var _doRecycle = function(_item,_index,_list){
            _item._$recycle();
            _list.splice(_index,1);
        };
        return function(_instance){
            if (!_instance) return null;
            if (!_u._$isArray(_instance)){
// instance is not instanceof class
                if (!(_instance instanceof this)){
// use constructor recycle instance
                    var _class = _instance.constructor;
                    if (!!_class._$recycle){
                        _class._$recycle(_instance);
                    }
                    return null;
                }
// delete singleton instance
                if (_instance==this.__instance){
                    delete this.__instance;
                }
                if (_instance==this.__inctanse){
                    delete this.__inctanse;
                }
// do recycle
                _instance.__destroy();
// recycle instance
                if (!this.__pool){
                    this.__pool = [];
                }
                if (_u._$indexOf(this.__pool,_instance)<0){
                    this.__pool.push(_instance);
                }
                return null;
            }
// recycle instance array
            _u._$reverseEach(_instance,_doRecycle,this);
        };
    })();
    /**
     * 取控件实例（单例），如果控件指明了为单例模式，
     * 则项目中使用该控件时统一使用此接口获取控件实例，使用方式同_$allocate
     *
     * ```javascript
     *   // 取控件单例，确保在第一次取单例时输入所有配置参数
     *   var _widget = _p._$$Widget._$getInstance({
*       conf0:'aaaaaaa',
*       conf1:'bbbbbbbbbbbbb',
*       onxxx:function(){
*           // TODO something
*       }
*   });
     *
     *   // 后续取单例忽略配置参数
     *   var _widget1 = _p._$$Widget._$getInstance({
*       conf0:'bbbbb'  // <-- 如果单例已生成，则这里的配置信息不会生效
*   });
     *
     *   // 等价于如下调用
     *   var _widget2 = _p._$$Widget._$getInstance();
     * ```
     *
     * @method module:util/event._$$EventTarget._$getInstance
     * @see    module:util/event._$$EventTarget._$getInstanceWithReset
     * @see    module:util/event._$$EventTarget._$allocate
     * @param  {Object}  arg0 - 配置参数，根据控件实际情况提供配置参数支持
     * @return {module:util/event._$$EventTarget} 控件实例
     */
    _p._$$EventTarget._$getInstance = function(_options){
        if (!this.__instance){
            this.__instance = this._$allocate(_options);
        }
        return this.__instance;
    };
    /**
     * 取控件实例（单例），如果控件指明了为单例模式，
     * 则项目中使用该控件时统一使用此接口获取控件实例，使用方式同_$getInstance，
     * 该接口同_$getInstance接口的主要区别在于输入的配置参数是否在每次调用接口时都重置
     *
     * ```javascript
     *   // 取控件单例，确保在第一次取单例时输入所有配置参数
     *   var _widget = _p._$$Widget._$getInstanceWithReset({
*       conf0:'aaaaaaa',
*       conf1:'bbbbbbbbbbbbb',
*       onxxx:function(){
*           // TODO something
*       }
*   });
     *
     *   // 后续取单例使用新的配置参数
     *   var _widget1 = _p._$$Widget._$getInstanceWithReset({
*       conf0:'bbbbb'  // <-- 如果单例已生成，则重置这里的配置信息
*   });
     * ```
     *
     * @method module:util/event._$$EventTarget._$getInstanceWithReset
     * @see    module:util/event._$$EventTarget._$getInstance
     * @see    module:util/event._$$EventTarget._$allocate
     * @param  {Object}  arg0 - 配置参数，根据控件实际情况提供配置参数支持
     * @param  {Boolean} arg1 - 是否需要先清理已有实例
     * @return {module:util/event._$$EventTarget} 控件实例
     */
    _p._$$EventTarget._$getInstanceWithReset = function(_options,_clear){
// clear instance
        if (!!_clear&&!!this.__inctanse){
            this.__inctanse._$recycle();
            delete this.__inctanse;
        }
// allocate instance
        if (!this.__inctanse){
            this.__inctanse = this._$allocate(_options);
        }else{
            this.__inctanse.__reset(_options);
        }
        return this.__inctanse;
    };
    /**
     * 控件初始化，
     * 子类可重写此接口业务逻辑，
     * 子类可通过调用__super接口调用父类的初始化业务逻辑
     *
     * ```javascript
     *   // 子类控件初始化业务逻辑
     *   _pro.__init = function(){
*       // 调用父类控件初始化
*       this.__super();
*       // TODO something
*   };
     * ```
     *
     * @protected
     * @method module:util/event._$$EventTarget#__init
     * @return {Void}
     */
    _pro.__init = function(){
        this.__events = {};
        this.__events_dom = {};
        this.id = _u._$uniqueID();
    };
    /**
     * 控件重置，此接口用来接收控件配置参数的处理，
     * 控件基类已处理以下业务逻辑：
     *
     * * 缓存通过配置参数输入的回调事件
     *
     * 子类重写此接口业务逻辑来处理具体控件对配置参数的处理，
     * 子类通过调用__super接口调用父类的重置业务逻辑
     *
     * ```javascript
     *   // 子类控件重置业务逻辑
     *   _pro.__reset = function(_options){
*       // 调用父类控件重置逻辑
*       this.__super(_options);
*       // TODO something
*   };
     * ```
     *
     * @protected
     * @method module:util/event._$$EventTarget#__reset
     * @param  {Object} arg0 - 配置参数，根据控件实际情况提供配置参数支持
     * @return {Void}
     */
    _pro.__reset = function(_options){
        this._$batEvent(_options);
    };
    /**
     * 控件销毁，当控件在回收时会调用此接口，基类已处理以下业务逻辑：
     *
     * * 通过配置参数输入的事件回调的清理
     * * 通过__doInitDomEvent接口添加的DOM事件的清理
     *
     * 一般情况下控件还需回收通过重置接口__reset产生的数据，
     * 子类可重写此接口业务逻辑来触发onbeforerecycle和onafterrecycle事件，
     * 子类可通过调用__super接口调用父类的销毁业务逻辑
     *
     * ```javascript
     *   // 子类重写控件销毁逻辑
     *   _pro.__destroy = function(){
*       // 触发回收之前事件
*       this._$dispatchEvent('onbeforerecycle');
*       // 调用父类清理逻辑，如���有触发回收之后事件则以下业务逻辑需在触发回收之后事件后面调用
*       //this.__super();
*       // 清理本控件的数据
*       delete this.__conf0;
*       this.__widget2 = this.__widget2._$recycle();
*       // 触发回收之后事件，确保在onafterrecycle事件被清理前触发
*       this._$dispatchEvent('onafterrecycle');
*       this.__super();
*   };
     * ```
     *
     * @protected
     * @method module:util/event._$$EventTarget#__destroy
     * @return {Void}
     */
    _pro.__destroy = function(){
        this._$clearEvent();
        this.__doClearDomEvent();
    };
    /**
     * 初始化事件，
     * 重置接口__reset中需要通过_$addEvent接口添加的事件，
     * 使用此接口添加可以在回收时自动被清理
     *
     * ```javascript
     *   // 子类重置接口添加节点事件
     *   _pro.__reset = function(_options){
*       this.__super(_options);
*       // 添加DOM事件或者自定义事件
*       this.__doInitDomEvent([
*           [document,'click',this.__onDocClick._$bind(this)],
*           [window,'ok',this.__onWindowOK._$bind(this)]
*       ]);
*   };
     * ```
     *
     * @protected
     * @method module:util/event._$$EventTarget#__doInitDomEvent
     * @see    module:util/event._$$EventTarget#__doClearDomEvent
     * @param  {Array} arg0 - 待添加的事件配置列表
     * @return {Void}
     */
    _pro.__doInitDomEvent = (function(){
        var _doAttach = function(_args){
            if (!_args||_args.length<3) return;
            this.__events_dom['de-'+_u._$uniqueID()] = _args;
            _v._$addEvent.apply(_v,_args);
        };
        return function(_list){
            _u._$forEach(_list,_doAttach,this);
        };
    })();
    /**
     * 清除DOM事件，_$recycle接口会自动调用来清理这种DOM事件
     *
     * ```javascript
     *   // 子类重置接口清理节点事件
     *   _pro.__destroy = function(_options){
*       this.__doClearDomEvent();
*       this.__super(_options);
*   };
     * ```
     *
     * @protected
     * @method module:util/event._$$EventTarget#__doClearDomEvent
     * @see    module:util/event._$$EventTarget#__doInitDomEvent
     * @return {Void}
     */
    _pro.__doClearDomEvent = (function(){
        var _doRemoveEvent = function(_args,_key,_map){
            delete _map[_key];
            _v._$delEvent.apply(_v,_args);
        };
        return function(){
            _u._$loop(this.__events_dom,_doRemoveEvent);
        };
    })();
    /**
     * 清理所有组合的控件
     *
     * ```javascript
     *   // 子类重置接口清理组件
     *   _pro.__destroy = function(_options){
*       this.__doClearComponent(function(_inst){
*           // 不回收_p._$$Widget2控件实例
*           return _inst instanceof _p._$$Widget2;
*       });
*       this.__super(_options);
*   };
     * ```
     *
     * @protected
     * @method module:util/event._$$EventTarget#__doClearComponent
     * @param  {Function} arg0 - 过滤接口，返回true表示不清理该控件
     * @return {Void}
     */
    _pro.__doClearComponent = function(_filter){
        _filter = _filter||_f;
        _u._$loop(this,function(_inst,_key,_map){
            if (!!_inst&&!!_inst._$recycle&&!_filter(_inst)){
                delete _map[_key];
                _inst._$recycle();
            }
        });
    };
    /**
     * 回收控件，通过实例的构造类来回收当前实例
     *
     * ```javascript
     *   // 通过实例的接口回收当前实例
     *   _widget._$recycle();
     * ```
     *
     * @method module:util/event._$$EventTarget#_$recycle
     * @see    module:util/event._$$EventTarget#_$allocate
     * @return {Void}
     */
    _pro._$recycle = function(){
        this.constructor._$recycle(this);
    };
    /**
     * 判断是否有注册事件回调
     *
     * ```javascript
     *   // 分配实例
     *   var _widget = _p._$$Widget._$allocate({
*       onok:function(){
*           // TODO
*       }
*   });
     *   // 判断控件实例是否注册有onok事件回调
     *   _widget._$hasEvent('onok');
     * ```
     *
     * @method module:util/event._$$EventTarget#_$hasEvent
     * @param  {String} arg0 - 事件类型
     * @return {Boolean}       是否注册了事件回调
     */
    _pro._$hasEvent = function(_type){
        var _type = (_type||'').toLowerCase(),
            _event = this.__events[_type];
        return !!_event&&_event!==_f;
    };
    /**
     * 删除单个事件回调
     *
     * ```javascript
     *   var _handler = function(){
*       // TODO
*   };
     *   // ��配实例
     *   var _widget = _p._$$Widget._$allocate({
*       onok:_handler
*   });
     *   // 删除onok事件回调
     *   _widget._$delEvent('onok',_handler);
     * ```
     *
     * @method module:util/event._$$EventTarget#_$delEvent
     * @param  {String}   arg0 - 事件类型
     * @param  {Function} arg1 - 事件处理函数
     * @return {Void}
     */
    _pro._$delEvent = function(_type,_event){
        var _type = (_type||'').toLowerCase(),
            _events = this.__events[_type];
        if (!_u._$isArray(_events)){
            if (_events==_event){
                delete this.__events[_type];
            }
            return;
        }
// batch remove
        _u._$reverseEach(
            _events,function(_func,_index,_list){
                if (_func==_event){
                    _list.splice(_index,1);
                }
            }
        );
        if (!_events.length){
            delete this.__events[_type];
        }
    };
    /**
     * 重置事件，覆盖原有事件
     *
     * ```javascript
     *   // 分配实例
     *   var _widget = _p._$$Widget._$allocate();
     *   // 设置控件事件回调
     *   _widget._$setEvent('onok',function(){
*       // TODO something
*   });
     *   _widget._$setEvent('oncancel',function(){
*       // TODO something
*   });
     * ```
     *
     * @method module:util/event._$$EventTarget#_$setEvent
     * @param  {String}   arg0 - 事件类型，大小写不敏感
     * @param  {Function} arg1 - 事件处理函数
     * @return {Void}
     */
    _pro._$setEvent = function(_type,_event){
        if (!!_type&&_u._$isFunction(_event)){
            this.__events[_type.toLowerCase()] = _event;
        }
    };
    /**
     * 批量添加事件
     *
     * ```javascript
     *   // 分配实例
     *   var _widget = _p._$$Widget._$allocate();
     *   // 批量设置控件事件回调
     *   _widget._$batEvent({
*       onok:function(){
*           // TODO something
*       },
*       oncancel:function(){
*           // TODO something
*       }
*   });
     * ```
     *
     * @method module:util/event._$$EventTarget#_$batEvent
     * @see    module:util/event._$$EventTarget#_$setEvent
     * @param  {Object} arg0 - 事件集合,{type:function}
     * @return {Void}
     */
    _pro._$batEvent = (function(){
        var _doSetEvent = function(_event,_type){
            this._$setEvent(_type,_event);
        };
        return function(_events){
            _u._$loop(_events,_doSetEvent,this);
        };
    })();
    /**
     * 清除事件，没有指定类型则清除所有事件
     *
     * ```javascript
     *   // 分配实例
     *   var _widget = _p._$$Widget._$allocate({
*       onok:function(){
*           // TODO something
*       }
*   });
     *   // 清除onok事件回调
     *   _widget._$clearEvent('onok');
     *   // 清除所有时间回调
     *   _widget._$clearEvent();
     * ```
     *
     * @method module:util/event._$$EventTarget#_$clearEvent
     * @param  {String} arg0 - 事件类型
     * @return {Void}
     */
    _pro._$clearEvent = (function(){
        var _doClearEvent = function(_event,_type){
            this._$clearEvent(_type);
        };
        return function(_type){
            var _type = (_type||'').toLowerCase();
            if (!!_type){
                delete this.__events[_type];
            }else{
                _u._$loop(this.__events,_doClearEvent,this);
            }
        };
    })();
    /**
     * 追加事件，通过此接口可以对同一个事件添加多个回调函数
     *
     * ```javascript
     *   // 分配实例
     *   var _widget = _p._$$Widget._$allocate({
*       onok:function(){
*           // TODO something
*       }
*   });
     *   // 追加事件回调
     *   _widget._$addEvent({
*       onok:function(){
*           // TODO something
*       }
*   });
     * ```
     *
     * @method module:util/event._$$EventTarget#_$addEvent
     * @param  {String}   arg0 - 事件类型
     * @param  {Function} arg1 - 事件处理函数
     * @return {Void}
     */
    _pro._$addEvent = function(_type,_event){
// check type and event
        if (!_type||!_u._$isFunction(_event)){
            return;
        }
// cache event
        _type = _type.toLowerCase();
        var _events = this.__events[_type];
        if (!_events){
            this.__events[_type] = _event;
            return;
        }
        if (!_u._$isArray(_events)){
            this.__events[_type] = [_events];
        }
        this.__events[_type].push(_event);
    };
    /**
     * 调用事件，一般在控件实现的具体业务逻辑中使用
     *
     * ```javascript
     *   // 分配实例
     *   var _widget = _p._$$Widget._$allocate({
*       onok:function(){
*           // TODO something
*       }
*   });
     *   // 触发控件onok事件
     *   _widget._$dispatchEvent('onok');
     *
     *   // 在控件实现的业务逻辑中使用
     *   _pro.__doSomething = function(){
*       // TODO something
*       // 触发onok事件
*       this._$dispatchEvent('onok');
*   };
     * ```
     *
     * @method module:util/event._$$EventTarget#_$dispatchEvent
     * @param  {String}   arg0 - 事件类型，不区分大小写
     * @param  {Variable} arg1 - 事件可接受参数，具体看调用时的业务逻辑
     * @return {Void}
     */
    _pro._$dispatchEvent = function(_type){
        var _type = (_type||'').toLowerCase(),
            _event = this.__events[_type];
        if (!_event) return;
        var _args = _r.slice.call(arguments,1);
// single event
        if (!_u._$isArray(_event)){
            _event.apply(this,_args);
            return;
        }
// event list
        _u._$forEach(
            _event,function(_handler){
                if (DEBUG){
                    _handler.apply(this,_args);
                }else{
                    try{
                        _handler.apply(this,_args);
                    }catch(ex){
// ignore
                        console.error(ex.message);
                        console.error(ex.stack);
                    }
                }
            },this
        );
    };
    if (CMPT){
        _p._$$Event = _p._$$EventTarget;
        NEJ.copy(NEJ.P('nej.ut'),_p);
    }
    return _p;
},14,1,3,2);




I$(36,function (NEJ,_k,_e,_v,_u,_t,_p,_o,_f,_r){
    var _pro;
    /**
     * 自定义事件封装对象，封装的事件支持通过事件相关接口进行添加、删除等操作
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'base/event'
     *     'util/event'
     * ],function(_v,_t){
*     // 支持自定义事件
*     _t._$$CustomEvent._$allocate({
*         element:window,
*         event:'ok'
*     });
*
*     // 添加自定义事件
*     _v._$addEvent(window,'ok',function(){alert(0);});
*     _v._$addEvent(window,'ok',function(){alert(1);});
*
*     // 删除自定义事件
*     _v._$delEvent(window,'ok',function(){alert(0);});
*     _v._$clearEvent(window,'ok');
*
*     // 触发自定义事件
*     window.onok({a:'aaaaa'});
*     _v._$dispatchEvent(window,'ok',{a:'aaaaa'});
* });
     * ```
     *
     * @class    module:util/event/event._$$CustomEvent
     * @extends  module:util/event._$$EventTarget
     *
     * @param    {Object}       config  - 可选配置参数
     * @property {String|Node}  element - 事件关联节点ID或者对象，默认为window对象
     * @property {String|Array} event   - 事件名称或者名称列表
     */
    /**
     * 初始化时触发事件
     *
     * @event module:util/event/event._$$CustomEvent#oninit
     * @param {Object} event - 事件信息
     */
    /**
     * 事件调度前触发事件
     *
     * @event    module:util/event/event._$$CustomEvent#ondispatch
     * @param    {Object} event - 事件信息
     * @property {String} type  - 事件类型
     */
    /**
     * 添加事件时触发事件
     *
     * @event    module:util/event/event._$$CustomEvent#oneventadd
     * @param    {Object}   event    - 事件信息
     * @property {String}   type     - 事件类型
     * @property {Function} listener - 事件执行函数
     */
    _p._$$CustomEvent = _k._$klass();
    _pro = _p._$$CustomEvent._$extend(_t._$$EventTarget);
    /**
     * 控件初始化
     *
     * @protected
     * @method module:util/event/event._$$CustomEvent#__init
     * @return {Void}
     */
    _pro.__init = function(){
// onxxx - event entry handler
//   xxx - event callback handler list
        this.__cache = {};
        this.__super();
    };
    /**
     * 控件���置
     *
     * @protected
     * @method module:util/event/event._$$CustomEvent#__reset
     * @param  {Object} arg0 - 可选配置参数
     * @return {Void}
     */
    _pro.__reset = function(_options){
        this.__super(_options);
        this.__element = _e._$get(_options.element)||window;
// init event
        this.__doEventInit(_options.event);
        this.__doEventAPIEnhance();
        this._$dispatchEvent('oninit');
    };
    /**
     * 销毁控件
     *
     * @protected
     * @method module:util/event/event._$$CustomEvent#__destroy
     * @return {Void}
     */
    _pro.__destroy = (function(){
        var _doClear = function(_value,_key,_map){
            if (!_u._$isArray(_value)){
                _u._$safeDelete(this.__element,_key);
            }
            delete _map[_key];
        };
        return function(){
            this.__super();
// clear cache
            _u._$loop(
                this.__cache,_doClear,this
            );
            delete this.__element;
        };
    })();
    /**
     * 判断是否需要代理事件
     *
     * @protected
     * @method module:util/event/event._$$CustomEvent#__isDelegate
     * @param  {String|Node} arg0 - 节点
     * @param  {String}      arg1 - 事件
     * @return {Boolean}            是否需要代理事件
     */
    _pro.__isDelegate = function(_element,_type){
        _element = _e._$get(_element);
        return _element===this.__element&&
            (!_type||!!this.__cache['on'+_type]);
    };
    /**
     * 初始化事件
     *
     * @protected
     * @method module:util/event/event._$$CustomEvent#__doEventInit
     * @param  {String} arg0 - 事件名称
     * @return {Void}
     */
    _pro.__doEventInit = function(_event){
        if (_u._$isString(_event)){
            var _name = 'on'+_event;
            if (!this.__cache[_name]){
                this.__cache[_name] =
                    this.__doEventDispatch.
                        _$bind(this,_event);
            }
            this.__doEventBind(_event);
            return;
        }
        if (_u._$isArray(_event)){
            _u._$forEach(
                _event,this.__doEventInit,this
            );
        }
    };
    /**
     * 绑定事件
     *
     * @protected
     * @method module:util/event/event._$$CustomEvent#__doEventBind
     * @param  {String} arg0 - 事件名称
     * @return {Void}
     */
    _pro.__doEventBind = function(_type){
        var _event = 'on'+_type,
            _handler = this.__element[_event],
            _handler1 = this.__cache[_event];
        if (_handler!=_handler1){
            this.__doEventDelete(_type);
            if (!!_handler&&_handler!=_f){
                this.__doEventAdd(_type,_handler);
            }
            this.__element[_event] = _handler1;
        }
    };
    /**
     * 添加事件
     *
     * protected
     * @method module:util/event/event._$$CustomEvent#__doEventAdd
     * @param  {String}   arg0 - 事件名称
     * @param  {Function} arg1 - 事件回调
     * @return {Void}
     */
    _pro.__doEventAdd = function(_type,_handler,_front){
        var _list = this.__cache[_type];
        if (!_list){
            _list = [];
            this.__cache[_type] = _list;
        }
        if (_u._$isFunction(_handler)){
            !_front ? _list.push(_handler)
                : _list.unshift(_handler);
        }
    };
    /**
     * 删除事件
     *
     * protected
     * @method module:util/event/event._$$CustomEvent#__doEventDelete
     * @param  {String}   arg0 - 事件名称
     * @param  {Function} arg1 - 事件回调
     * @return {Void}
     */
    _pro.__doEventDelete = function(_type,_handler){
        var _list = this.__cache[_type];
        if (!_list||!_list.length) return;
// clear all event handler
        if (!_handler){
            delete this.__cache[_type];
            return;
        }
// delete one event handler
        _u._$reverseEach(
            _list,function(_value,_index,_xlist){
                if (_handler===_value){
                    _xlist.splice(_index,1);
                    return !0;
                }
            }
        );
    };
    /**
     * 事件调度
     *
     * protected
     * @method module:util/event/event._$$CustomEvent#__doEventDispatch
     * @param  {String} arg0 - 事件名称
     * @param  {Object} arg1 - 事件对象
     * @return {Void}
     */
    _pro.__doEventDispatch = function(_type,_event){
        _event = _event||{noargs:!0};
        if (_event==_o){
            _event = {};
        }
        _event.type = _type;
        this._$dispatchEvent('ondispatch',_event);
        if (!!_event.stopped) return;
        _u._$forEach(
            this.__cache[_type],function(_handler){
                if (DEBUG){
                    _handler(_event);
                }else{
                    try{
                        _handler(_event);
                    }catch(ex){
// ignore
                        console.error(ex.message);
                        console.error(ex.stack);
                    }
                }
            }
        );
    };
    /**
     * 增强事件操作API
     *
     * protected
     * @method module:util/event/event._$$CustomEvent#__doEventAPIEnhance
     * @return {Void}
     */
    _pro.__doEventAPIEnhance = (function(){
        var _doAddEvent = function(_event){
            var _args = _event.args,
                _type = _args[1].toLowerCase();
            if (this.__isDelegate(_args[0],_type)){
                _event.stopped = !0;
                this.__doEventBind(_type);
                this.__doEventAdd(_type,_args[2],_args[3]);
                this._$dispatchEvent('oneventadd',{
                    type:_type,
                    listener:_args[2]
                });
            }
        };
        var _doDelEvent = function(_event){
            var _args = _event.args,
                _type = _args[1].toLowerCase();
            if (this.__isDelegate(_args[0],_type)){
                _event.stopped = !0;
                this.__doEventDelete(_type,_args[2]);
            }
        };
        var _doClearEvent = function(_event){
            var _args = _event.args,
                _type = (_args[1]||'').toLowerCase();
            if (this.__isDelegate(_args[0])){
                if (!!_type){
                    this.__doEventDelete(_type);
                    return;
                }
                _u._$loop(
                    this.__cache,function(_value,_key){
                        if (_u._$isArray(_value)){
                            this.__doEventDelete(_key);
                        }
                    },this
                );
            }
        };
        var _doDispatchEvent = function(_event){
            var _args = _event.args,
                _type = _args[1].toLowerCase();
            if (this.__isDelegate(_args[0],_type)){
                _event.stopped = !0;
                _args[0]['on'+_type].apply(_args[0],_args.slice(2));
            }
        };
        return function(){
// void multi-enhance
            if (!!this.__enhanced){
                return;
            }
// enhance event api
            this.__enhanced = true;
            _v._$addEvent = _v._$addEvent._$aop(_doAddEvent._$bind(this));
            _v._$delEvent = _v._$delEvent._$aop(_doDelEvent._$bind(this));
            _v._$clearEvent = _v._$clearEvent._$aop(_doClearEvent._$bind(this));
            _v._$dispatchEvent = _v._$dispatchEvent._$aop(_doDispatchEvent._$bind(this));
            if (CMPT){
                NEJ.copy(NEJ.P('nej.v'),_v);
            }
        };
    })();
    if (CMPT){
        NEJ.copy(NEJ.P('nej.ut'),_p);
    }
    return _p;
},14,1,4,3,2,30);
I$(44,function (NEJ,_k,_g,_v,_u,_t,_p,_o,_f,_r){
    var _pro,
        _timeout = 60000;
    /**
     * 资源加载器
     *
     * @class    module:util/ajax/loader/loader._$$LoaderAbstract
     * @extends  module:util/event._$$EventTarget
     *
     * @param    {Object} config  - 可选配置参数
     * @property {String} version - 版本信息
     * @property {Number} timeout - 超时时间，0表示禁止超时监测
     */
    /**
     * 资源载入失败回调
     *
     * @event    module:util/ajax/loader/loader._$$LoaderAbstract#onerror
     * @param    {Object} event   - 错误信息
     * @property {Number} code    - 错误码
     * @property {String} message - 错误信息
     */
    /**
     * 资源载入成功回调
     *
     * @event  module:util/ajax/loader/loader._$$LoaderAbstract#onload
     * @param  {Variable} event - 请求返回数据
     */
    /**
     * 资源加载中回调
     *
     * @event  module:util/ajax/loader/loader._$$LoaderAbstract#onloading
     */
    _p._$$LoaderAbstract = _k._$klass();
    _pro = _p._$$LoaderAbstract._$extend(_t._$$EventTarget);
    /**
     * 控件初始化
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__init
     * @return {Void}
     */
    _pro.__init = function(){
        this.__super();
        this.__qopt = {
            onerror:this.__onQueueError._$bind(this),
            onload:this.__onQueueLoaded._$bind(this)
        };
        if (!this.constructor.__cache){
// url : {request:script,timer:2,bind:[instance1,instance2 ... ]}
// key : {error:0,loaded:0,total:0,bind:[instance1,instance2 ... ]}
            this.constructor.__cache = {loaded:{}};
        }
    };
    /**
     * 控件重置
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__reset
     * @param  {Object} arg0 - 可选配置参数
     * @return {Void}
     */
    _pro.__reset = function(_options){
        this.__super(_options);
        this.__version = _options.version;
        this.__timeout = _options.timeout;
        this.__qopt.version = this.__version;
        this.__qopt.timeout = this.__timeout;
    };
    /**
     * 删除加载信息
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__delLoadData
     * @param  {String} arg0 - 标识
     * @return {Object}        加载信息
     */
    _pro.__delLoadData = function(_key){
        delete this.constructor.__cache[_key];
    };
    /**
     * 取加载信息
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__getLoadData
     * @param  {String} arg0 - 标识
     * @return {Object}        加载信息
     */
    _pro.__getLoadData = function(_key){
        return this.constructor.__cache[_key];
    };
    /**
     * 设置加载信息
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__setLoadData
     * @param  {String} arg0 - 标识
     * @param  {Object} arg1 - 加载信息
     * @return {Void}
     */
    _pro.__setLoadData = function(_key,_data){
        this.constructor.__cache[_key] = _data;
    };
    /**
     * 取资源载入控件，子类实现具体逻辑
     *
     * @abstract
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__getRequest
     * @return {Script|Link} 控件
     */
    _pro.__getRequest = _f;
    /**
     * 清理控件
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__doClearRequest
     * @param  {Script|Link} arg0 - 控件
     * @return {Void}
     */
    _pro.__doClearRequest = function(_request){
        _v._$clearEvent(_request);
    };
    /**
     * 资源载入
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__doRequest
     * @param  {Script|Link} arg0 - 控件
     * @return {Void}
     */
    _pro.__doRequest = function(_request){
        _request.src = this.__url;
        document.head.appendChild(_request);
    };
    /**
     * 执行清理任务
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__doClear
     * @return {Void}
     */
    _pro.__doClear = function(){
        var _cache = this.__getLoadData(this.__url);
        if (!_cache) return;
        window.clearTimeout(_cache.timer);
        this.__doClearRequest(_cache.request);
        delete _cache.bind;
        delete _cache.timer;
        delete _cache.request;
        this.__delLoadData(this.__url);
        this.__getLoadData('loaded')[this.__url] = !0;
    };
    /**
     * 执行回调
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__doCallback
     * @param  {String} arg0 - 回调名称
     * @return {Void}
     */
    _pro.__doCallback = function(_name){
        var _cache = this.__getLoadData(this.__url);
        if (!_cache) return;
        var _list = _cache.bind;
        this.__doClear();
        if (!!_list&&_list.length>0){
            var _instance;
            while(_list.length){
                _instance = _list.shift();
                try{
                    _instance._$dispatchEvent(_name,arguments[1]);
                }catch(ex){
// ignore
                    if (DEBUG) throw ex;
                    console.error(ex.message);
                    console.error(ex.stack);
                }
                _instance._$recycle();
            }
        }
    };
    /**
     * 资源载入异常事件
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__onError
     * @param  {Object} arg0 - 错误信息
     * @return {Void}
     */
    _pro.__onError = function(_error){
        this.__doCallback('onerror',_error);
    };
    /**
     * 资源载入成功事件
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__onLoaded
     * @return {Void}
     */
    _pro.__onLoaded = function(){
        this.__doCallback('onload');
    };
    /**
     * 载入队列资源
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__doLoadQueue
     * @param  {String} arg0 - 资源地址
     * @return {Void}
     */
    _pro.__doLoadQueue = function(_url){
        this.constructor._$allocate(this.__qopt)._$load(_url);
    };
    /**
     * 检查队列状况
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__onQueueCheck
     * @return {Void}
     */
    _pro.__onQueueCheck = function(_error){
        var _cache = this.__getLoadData(this.__key);
        if (!_cache) return;
        if (!!_error)
            _cache.error++;
        _cache.loaded ++;
        if (_cache.loaded<_cache.total) return;
        this.__delLoadData(this.__key);
        this._$dispatchEvent(_cache.error>0?'onerror':'onload');
    };
    /**
     * 队列载入资源异常事件
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__onQueueError
     * @param  {Object} arg0 - 错误信息
     * @return {Void}
     */
    _pro.__onQueueError = function(_error){
        this.__onQueueCheck(!0);
    };
    /**
     * 队列载入资源成功事件
     *
     * @protected
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#__onQueueLoaded
     * @return {Void}
     */
    _pro.__onQueueLoaded = function(){
        this.__onQueueCheck();
    };
    /**
     * 载入资源
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/ajax/loader/html',
     *     'util/ajax/loader/style',
     *     'util/ajax/loader/script'
     * ],function(_t0,_t1,_t2){
*     // 载入指定html,10秒超时
*     var _loader = _t0._$$LoaderHtml._$allocate({
*         timeout:10000,
*         onload:function(){
*             // 载入资源成功的回调
*         }
*     });
*     // 绝对路径��者当前页面的相对路径
*     _loader._$load('../../../html/util/formTest.html');
*
*     // 载入指定script,20秒超时
*     var _loader = _t2._$$LoaderScript._$allocate({
*         timeout:20000,
*         onload:function(){
*             // 载入资源成功的回调
*         }
*     });
*     // 绝对路径或者当前页面的相对路径
*     _loader._$load('../../../javascript/log.js');
*
*     // 载入指定style,30秒超时
*     var _loader = _t1._$$LoaderStyle._$allocate({
*         timeout:30000,
*         onload:function(){
*             // 载入资源成功的回调
*         }
*     });
*     // 绝对路径或者当前页面的相对路径
*     _loader._$load('../../../base/qunit.css');
* });
     * ```
     *
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#_$load
     * @param  {String} arg0 - 资源地址
     * @return {Void}
     */
    _pro._$load = function(_url){
        _url = _u._$absolute(_url);
        if (!_url){
            this._$dispatchEvent('onerror',{
                code:_g._$CODE_NOTASGN,
                message:'请指定要载入的资源地址！'
            });
            return;
        };
        this.__url = _url;
        if (!!this.__version){
            this.__url += (this.__url.indexOf('?')<0?'?':'&')+this.__version;
        }
        if (this.__getLoadData('loaded')[this.__url]){
            try{
                this._$dispatchEvent('onload');
            }catch(ex){
// ignore
                if (DEBUG) throw ex;
                console.error(ex.message);
                console.error(ex.stack);
            }
            this._$recycle();
            return;
        }
        var _cache = this.__getLoadData(this.__url),_request;
        if (!!_cache){
            _cache.bind.unshift(this);
            _cache.timer = window.clearTimeout(_cache.timer);
        }else{
            _request = this.__getRequest();
            _cache = {request:_request,bind:[this]};
            this.__setLoadData(this.__url,_cache);
            _v._$addEvent(
                _request,'load',
                this.__onLoaded._$bind(this)
            );
            _v._$addEvent(
                _request,'error',
                this.__onError._$bind(this,{
                    code:_g._$CODE_ERRSERV,
                    message:'无法加载指定资源文件['+this.__url+']！'
                })
            );
        }
        if (this.__timeout!=0){
            _cache.timer = window.setTimeout(
                this.__onError._$bind(this,{
                    code:_g._$CODE_TIMEOUT,
                    message:'指定资源文件['+this.__url+']载入超时！'
                }),
                this.__timeout||_timeout
            );
        }
        if (!!_request){
            this.__doRequest(_request);
        }
        this._$dispatchEvent('onloading');
    };
    /**
     * 队列载入资源
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/ajax/loader/html.js'
     * ],function(_t){
*     var _loader = _t._$$LoaderHtml._$allocate({
*         onload:function(){
*             // 载入队列资源成功的回调
*         }
*     });
*     // 路径列表，可以是绝对路径也可以是当前页面的相对路径
*     var _list = [
*         '../../../html/util/formTest.html',
*         '../../../html/util/cacheTest.html'
*     ];
*     _loader._$queue(_list);
* });
     * ```
     *
     * @method module:util/ajax/loader/loader._$$LoaderAbstract#_$queue
     * @param  {Array} arg0 - 资源地址队列
     * @return {Void}
     */
    _pro._$queue = function(_list){
        if (!_list||!_list.length){
            this._$dispatchEvent('onerror',{
                code:_g._$CODE_NOTASGN,
                message:'请指定要载入的资源队列！'
            });
            return;
        }
        this.__key = _u._$uniqueID();
        var _cache = {error:0,loaded:0,total:_list.length};
        this.__setLoadData(this.__key,_cache);
        _u._$forEach(
            _list,function(v,i){
                if (!v){
                    _cache.total--;
                    return;
                }
                this.__doLoadQueue(v);
            },this
        );
        this._$dispatchEvent('onloading');
    };
    return _p;
},14,1,20,3,2,30);





I$(7,function (_e,ut,e, e2,BaseComponent,Topbar,Toast,_am,_p,_o,_f,_r,_pro) {
    _p._$$Module = NEJ.C();
    _pro = _p._$$Module._$extend(ut._$$EventTarget);
    _pro.__init = function(_options) {
        this.__supInit(_options);

        this._$seedAfterPageInit();
        _am._$$ActionManage._$allocate();
    };
    /**
     * added by hzliuxinqi 2015-7-10
     * 页面初始化完成后执行，主要用于部分不需要在页面显示后第一时间需要处理的操作，比如
     *   回到顶部，app下载条等
     * 也可以用来避免iOS平台第三方浏览器唤醒app时，当前页面的部分js被终止执行的问题。
     * 此函数通过setTimeout 的方式来执行，一般不会被iOS的墓碑机制给cancel
     * 函数具体执行内容需要子类实现
     */
    _pro._$afterPageInit = _f;
    _pro._$seedAfterPageInit = function(){
        var delay = 500; //延迟500ms开始执行
        if (this._$afterPageInit && this._$afterPageInit != _f) {
            setTimeout(this._$afterPageInit._$bind(this), delay);
        }
    };
    return _p._$$Module;
},4,30,31,28,32,33,11,34);




//******

I$(116,function (NEJ,_k,_t,_t0,_p,_o,_f,_r){
// variable declaration
    var _pro;
    /**
     * 动画基类
     *
     * @class   module:util/animation/animation._$$Animation
     * @extends module:util/event._$$EventTarget
     *
     * @param    {Object} config - 可选配置参数
     * @property {Object} to     - 动画结束信息
     * @property {Object} from   - 动画初始信息
     * @property {Number} delay  - 延时时间，单位毫秒，默认0
     */
    /**
     * 动画结束回调事件
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/animation/bounce'
     * ],function(_t){
*     var _bounce = _t._$$AnimBounce._$allocate({
*         from: {
*             offset: 100,
*             velocity: 100
*         },
*         acceleration:100,
*         onstop: function(){
*             // 动画停止后回收控件
*             _bounce = nej.ut._$$AnimBounce._$recycle(_bounce);
*         }
*     });
* });
     * ```
     *
     * @event module:util/animation/animation._$$Animation#onstop
     */
    /**
     * 动画过程回调事件
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/animation/bounce'
     * ],function(_t){
*     var _bounce = _t._$$AnimBounce._$allocate({
*         from: {
*             offset: 100,
*             velocity: 100
*         },
*         acceleration:100,
*         onupdate: function(_event){
*             // 坐标
*             console.log(_event.offset + 'px');
*             // 初速度
*             console.log(_event.velocity);
*         }
*     });
* });
     * ```
     *
     * @event    module:util/animation/animation._$$Animation#onupdate
     * @param    {Object} event    - 可选配置参数
     * @property {Number} offset   - 偏移量
     * @property {Number} velocity - 初速度(px/s)
     */
    _p._$$Animation = _k._$klass();
    _pro = _p._$$Animation._$extend(_t._$$EventTarget);
    /**
     * 控件重置
     *
     * @protected
     * @method   module:util/animation/animation._$$Animation#__reset
     * @param    {Object} arg0 - 可选配置参数
     * @property {Number} to   - 结束坐标
     * @property {Number} from - 起始坐标
     * @return   {Void}
     */
    _pro.__reset = function(_options){
        this.__super(_options);
        this.__end = _options.to||_o;
        this.__begin = _options.from||{};
        this.__delay = Math.max(
            0,parseInt(_options.delay)||0
        );
    };
    /**
     * 控件销毁
     *
     * @protected
     * @method module:util/animation/animation._$$Animation#__destroy
     * @return {Void}
     */
    _pro.__destroy = function(){
        this.__super();
        this._$stop();
        if (!!this.__dtime){
            window.clearTimeout(this.__dtime);
            delete this.__dtime;
        }
        delete this.__end;
        delete this.__begin;
    };
    /**
     * 动画帧逻辑
     *
     * @protected
     * @method module:util/animation/animation._$$Animation#__onAnimationFrame
     * @param  {Number} arg0 - 时间值
     * @return {Void}
     */
    _pro.__onAnimationFrame = function(_time){
        if (!this.__begin) return;
        if ((''+_time).indexOf('.')>=0){
            _time = +new Date;
        }
        if (this.__doAnimationFrame(_time)){
            this._$stop();
            return;
        }
        this.__timer = _t0.requestAnimationFrame(
            this.__onAnimationFrame._$bind(this)
        );
    };
    /**
     * 动画帧回调，子类实现具体算法
     *
     * @abstract
     * @method module:util/animation/animation._$$Animation#__doAnimationFrame
     * @param  {Number}  arg0 - 时间值
     * @return {Boolean}        是否停止动画
     */
    _pro.__doAnimationFrame = _f;
    /**
     * 注册动画监听事件
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/animation/bounce'
     * ],function(_t){
*     var _bounce = _t._$$AnimBounce._$allocate({
*         from: {
*             offset: 100,
*             velocity: 100
*         },
*         acceleration:100,
*         onupdate: function(_event){
*             // 坐标
*             console.log(_event.offset + 'px');
*             // 初速度
*             console.log(_event.velocity);
*         }
*     });
*     // 进行弹性动画
*     _bounce._$play();
* });
     * ```
     *
     * @method module:util/animation/animation._$$Animation#_$play
     * @return {Void}
     */
    _pro._$play = (function(){
        var _doPlayAnim = function(){
            this.__dtime = window.clearTimeout(this.__dtime);
            this.__begin.time = +new Date;
            this.__timer = _t0.requestAnimationFrame(
                this.__onAnimationFrame._$bind(this)
            );
        };
        return function(){
            this.__dtime = window.setTimeout(
                _doPlayAnim._$bind(this),
                this.__delay
            );
        };
    })();
    /**
     * 取消动画监听事件
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/animation/bounce'
     * ],function(_t){
*     var _bounce = _t._$$AnimBounce._$allocate({
*         from: {
*             offset: 100,
*             velocity: 100
*         },
*         acceleration:100,
*         onupdate: function(_event){
*             // 坐标
*             console.log(_event.offset + 'px');
*             // 初速度
*             console.log(_event.velocity);
*         }
*     });
*     // 进行动画
*     _bounce._$play();
*     // 停止动画,触发onstop
*     _bounce._$stop();
* });
     * ```
     *
     * @method module:util/animation/animation._$$Animation#_$stop
     * @return {Void}
     */
    _pro._$stop = function(){
        this.__timer = _t0.cancelAnimationFrame(this.__timer);
        this._$dispatchEvent('onstop');
    };
    if (CMPT){
        NEJ.copy(NEJ.P('nej.ut'),_p);
    }
    return _p;
},14,1,30,58);



I$(115,function (NEJ,_k,_u,_t0,_p,_o,_f,_r){
// variable declaration
    var _pro;
    /**
     * 贝塞尔曲线算法
     *
     * 初始信息包括
     *
     * * offset  [Number]  偏移量
     *
     * 结束信息包括
     *
     * * offset  [Number]  偏移量
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/animation/bezier'
     * ],function(_t){
*     var _easein = nej.ut._$$AnimBezier._$allocate({
*         from: {
*             offset: 100
*         },
*         to:{
*             offset: 0
*         },
*         timing:'easein',
*         onupdate:function(_event){
*             // 坐标
*             console.log(_event.offset + 'px');
*             // 更新节点位置
*         },
*         onstop:function(){
*             // 动画停止后回收控件
*             this._$recycle();
*         }
*     });
*     // 进行弹性动画
*     _easein._$play();
* });
     * ```
     *
     * @class    module:util/animation/bezier._$$AnimBezier
     * @extends  module:util/animation/animation._$$Animation
     *
     * @param    {Object} config   - 可选配置参数
     * @property {Number} duration - 持续时间，单位毫秒，默认为200ms
     * @property {String} timing   - 时间函数，默认为ease，ease/easein/easeout/easeinout/linear/cubic-bezier(x1,y1,x2,y2)
     */
    _p._$$AnimBezier = _k._$klass();
    _pro = _p._$$AnimBezier._$extend(_t0._$$Animation);
    /**
     * 控件重置
     *
     * @protected
     * @method module:util/animation/bezier._$$AnimBezier#__reset
     * @param  {Object} arg0 - 可选配置参数
     * @return {Void}
     */
    _pro.__reset = function(_options){
        this.__super(_options);
        this.__duration = _options.duration||200;
        this.__epsilon  = 1/(200*this.__duration);
        this.__doParseTiming(_options.timing);
        this.__doCalPolynomialCoefficients();
    };
    /**
     * 控件销毁
     *
     * @protected
     * @method module:util/animation/bezier._$$AnimBezier#__destroy
     * @return {Void}
     */
    _pro.__destroy = function(){
        this.__super();
        delete this.__pointer;
        delete this.__coefficient;
    };
    /**
     * 解析时间动画为坐标信息
     *
     * @protected
     * @method module:util/animation/bezier._$$AnimBezier#__doParseTiming
     * @param  {String} arg0 - 时间动画
     * @return {Void}
     */
    _pro.__doParseTiming = (function(){
        var _reg0 = /^cubic\-bezier\((.*?)\)$/i,
            _reg1 = /\s*,\s*/i,
            _pointers = {
                linear:[0,0,1,1]
                ,ease:[0.25,0.1,0.25,1.0]
                ,easein:[0.42,0,1,1]
                ,easeout:[0,0,0.58,1]
                ,easeinout:[0,0,0.58,1]
            };
        var _doParseFloat = function(_value,_index,_list){
            _list[_index] = parseFloat(_value);
        };
        return function(_timing){
            _timing = (_timing||'').toLowerCase();
            this.__pointer = _pointers[_timing];
            if (_reg0.test(_timing)){
                this.__pointer = RegExp.$1.split(_reg1);
                _u._$forEach(this.__pointer,_doParseFloat);
            }
            if (!!this.__pointer) return;
            this.__pointer = _pointers.ease;
        };
    })();
    /**
     * 计算贝塞尔曲线多项式系数
     *
     * @protected
     * @method module:util/animation/bezier._$$AnimBezier#__doCalPolynomialCoefficients
     * @return {Void}
     */
    _pro.__doCalPolynomialCoefficients = function(){
        var _pt = this.__pointer,
            _cx = 3*_pt[0],
            _bx = 3*(_pt[2]-_pt[0])-_cx,
            _ax = 1-_cx-_bx,
            _cy = 3*_pt[1],
            _by = 3*(_pt[3]-_pt[1])-_cy,
            _ay = 1-_cy-_by;
        this.__coefficient = {
            ax:_ax, ay:_ay,
            bx:_bx, by:_by,
            cx:_cx, cy:_cy
        };
    };
    /**
     * 计算目标接近率
     *
     * @protected
     * @method module:util/animation/bezier._$$AnimBezier#__doCalCubicBezierAtTime
     * @param  {Number} arg0 - 当前时间
     * @return {Float}         终点接近率
     */
    _pro.__doCalCubicBezierAtTime = (function(){
        var _doSampleCurveX = function(_time,_coef){
            return ((_coef.ax*_time+_coef.bx)*_time+_coef.cx)*_time;
        };
        var _doSampleCurveY = function(_time,_coef){
            return ((_coef.ay*_time+_coef.by)*_time+_coef.cy)*_time;
        };
        var _doSampleCurveDerivativeX = function(_time,_coef){
            return (3*_coef.ax*_time+2*_coef.bx)*_time+_coef.cx;
        };
        var _doSolveCurveX = function(_time,_epsilon,_coef){
            var t0,t1,t2,x2,d2,i;
// First try a few iterations of Newton's method -- normally very fast.
            for(t2=_time,i=0;i<8;i++){
                x2 = _doSampleCurveX(t2,_coef)-_time;
                if (Math.abs(x2)<_epsilon)
                    return t2;
                d2 = _doSampleCurveDerivativeX(t2,_coef);
                if (Math.abs(d2)<1e-6)
                    break;
                t2 = t2-x2/d2;
            }
// Fall back to the bisection method for reliability.
            t0 = 0; t1 = 1; t2 = _time;
            if (t2<t0) return t0;
            if (t2>t1) return t1;
            while(t0<t1) {
                x2 = _doSampleCurveX(t2,_coef);
                if (Math.abs(x2-_time)<_epsilon)
                    return t2;
                if (_time>x2)
                    t0 = t2;
                else
                    t1 = t2;
                t2 = (t1-t0)*0.5+t0;
            }
// Failure.
            return t2;
        };
        return function(_delta){
            return _doSampleCurveY(
                _doSolveCurveX(_delta/this.__duration,
                    this.__epsilon,this.__coefficient),this.__coefficient);
        };
    })();
    /**
     * 动画帧回调
     *
     * @protected
     * @method module:util/animation/bezier._$$AnimBezier#__doAnimationFrame
     * @param  {Number} arg0 - 时间值
     * @return {Boolean}       是否停止
     */
    _pro.__doAnimationFrame = function(_time){
        var _delta   = _time-this.__begin.time,
            _percent = this.__doCalCubicBezierAtTime(_delta),
            _offset  = _u._$fixed(this.__begin.offset*(1-_percent)+
            this.__end.offset*_percent,2),
            _stop = !1;
// offset out of begin and end range
        if (_delta>=this.__duration){
            _offset = this.__end.offset;
            _stop = !0;
        }
        this._$dispatchEvent('onupdate',{
            offset:1*_offset
        });
        return _stop;
    };
    /**
     * 取消动画监听事件
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'util/animation/bezier'
     * ],function(_t){
*     var _easein = nej.ut._$$AnimBezier._$allocate({
*         from: {
*             offset: 100
*         },
*         to:{
*             offset: 0
*         },
*         timing:'easein',
*         onupdate: function(_event){
*             // 坐标
*             console.log(_event.offset + 'px');
*         }
*     });
*     // 进行弹性动画
*     _easein._$play();
*     // 结束动画
*     _easein._$stop();
* });
     * ```
     * @method module:util/animation/bezier._$$AnimBezier#_$stop
     * @return {Void}
     */
    _pro._$stop = function(){
        this._$dispatchEvent('onupdate',{
            offset:this.__end.offset
        });
        this.__super();
    };
    if (CMPT){
        NEJ.copy(NEJ.P('nej.ut'),_p);
    }
    return _p;
},14,1,2,116);
I$(114,function (NEJ,_k,_u,_t0,_p,_o,_f,_r){
// variable declaration
    var _pro;
    /**
     * 先快后慢动画
     *
     * 结构举例
     * ```html
     * <div id='id-bounce1'></div>
     * ```
     *
     * 脚本举例
     * ```javascript
     * NEJ.define([
     *     'pro/widget/util/timing'
     * ],function(_t){
*     // 创建动画实例
*     var _easeout  = _t._$$Timing._$allocate({
*         timing: 'easeout',
*         from:{
*             offset:100
*         },
*         to:{
*             offset:200
*         },
*         duration:1000,
*         onupdate:function(_event){
*             _box.style.left = _event.offset + 'px';
*         },
*         onstop:function(){
*             this._$recycle();
*         }
*     });
*     // 开始动画
*     _easeout._$play();
* });
     * ```
     *
     * @class   module:util/animation/easeout._$$Timing
     * @extends module:util/animation/bezier._$$AnimBezier
     *
     * @param   {Object} config 可选配置参数
     */
    _p._$$Timing = _k._$klass();
    _pro = _p._$$Timing._$extend(_t0._$$AnimBezier);
    /**
     * 控件重置
     *
     * @protected
     * @method module:util/animation/easeout._$$Timing#__reset
     * @param  {Object} arg0 - 可选配置参数
     * @return {Void}
     */
    _pro.__reset = function(_options){
        _options = _u._$merge({},_options);
        this.__super(_options);
        this.__polyfillRAF();
    };
    /**
     * 重置父类的动画帧逻辑
     *
     * @protected
     * @method module:util/animation/animation._$$Animation#__onAnimationFrame
     * @param  {Number} arg0 - 时间值
     * @return {Void}
     */
    _pro.__onAnimationFrame = function(_time){
        if (!this.__begin) return;
        if ((''+_time).indexOf('.')>=0){
            _time = +new Date;
        }
        if (this.__doAnimationFrame(_time)){
            this._$stop();
            return;
        }
        this.__timer = this.__requestAnimationFrame(
            this.__onAnimationFrame._$bind(this)
        );
    };
    _pro._$play = (function(){
        var _doPlayAnim = function(){
            this.__dtime = window.clearTimeout(this.__dtime);
            this.__begin.time = +new Date;
            this.__timer = this.__requestAnimationFrame(
                this.__onAnimationFrame._$bind(this)
            );
        };
        return function(){
            this.__dtime = window.setTimeout(
                _doPlayAnim._$bind(this),
                this.__delay
            );
        };
    })();
    _pro._$stop = function(){
        this.__timer = this.__cancelAnimationFrame(this.__timer);
        this._$dispatchEvent('onstop');
    };
    _pro.__polyfillRAF = function(){
        var lastTime = 0;
        var vendors = ['ms', 'moz', 'webkit', 'o'];
        var w = {};
        w.__requestAnimationFrame = window.requestAnimationFrame;
        w.__cancelAnimationFrame = window.cancelAnimationFrame;
        for(var x = 0; x < vendors.length && !w.__requestAnimationFrame; ++x) {
            w.__requestAnimationFrame = window[vendors[x]+'RequestAnimationFrame'];
            w.__cancelAnimationFrame = window[vendors[x]+'CancelAnimationFrame']
            || window[vendors[x]+'CancelRequestAnimationFrame'];
        }
        if (!w.__requestAnimationFrame)
            w.__requestAnimationFrame = function(callback) {
                var currTime = new Date().getTime();
                var timeToCall = Math.max(0, 16 - (currTime - lastTime));
                var id = window.setTimeout(function() { callback(currTime + timeToCall); },
                    timeToCall);
                lastTime = currTime + timeToCall;
                return id;
            };
        if (!w.__cancelAnimationFrame)
            w.__cancelAnimationFrame = function(id) {
                clearTimeout(id);
            };
        this.__requestAnimationFrame = function(callback){
            w.__requestAnimationFrame.apply(window, arguments);
        }
        this.__cancelAnimationFrame = function(id){
            w.__cancelAnimationFrame.apply(window, arguments);
        }
    };
    return _p;
},14,1,2,115);
I$(109,function (_k, _ut, $, _t, _ani) {
    var _p = {}, _pro;
    _p._$$Slider = _k._$klass();
    _pro = _p._$$Slider._$extend(_t._$$EventTarget);
    /**
     * 重置控件
     * @String/Node box : 滚动列表对象或者选择器 如：滚动元素为li的外层ul
     @object config : {
@Number width : 一次滚动宽度，默认为box里面第一个一级子元素宽度[如果子元素宽度不均匀则滚动效果会错乱]
     @Number size : 列表长度，默认为box里面所有一级子元素个数[如果size不等于一级子元素个数，则不支持循环滚动]
     @Boolean loop : 是否支持循环滚动 默认 true
     @Boolean auto : 是否自动滚动,支持自动滚动时必须支持循环滚动，否则设置无效,默认为true
     @Number slideInterval : 自动轮播一次时间间隔,默认为：3000ms
     @function callback : 可选参数，每次切换一幅图后的回调
     }
     */
    _pro.__reset = function(config) {
        this.box = $(config.box);
        this.config = config||{};
        this.width = this.config.width||this.box._$children()._$get(0).scrollWidth||document.body.clientWidth;//一次滚动的宽度
        this.size = this.config.size||this.box._$children().length;
        this.loop = (this.config.loop===undefined)||this.config.loop;//默认能循环滚动
        this.auto = (this.config.auto===undefined)||this.config.auto;//默认自动滚动
        this.slideInterval = this.config.slideInterval||3000;//轮播间隔
        this.scrollTime = this.config.scrollTime||300;//滚动时长
        this.minleft = -this.width*(this.size-1);//最小left值，注意是负数[不循环情况下的值]
        this.maxleft =0;//最大lfet值[不循环情况下的值]
        this.nowLeft = 0;//初始位置信息[不循环情况下的值]
        this.pointX = null;//记录一个x坐标
        this.pointY = null;//记录一个y坐标
        this.moveLeft = false;//记录向哪边滑动
        this.index = 0;
        this.busy = false;
        this.__touching = false; //用户是否正在进行触摸操作
        this.__action = '';
        this.point0 = {x:0,y:0};
        this.timer;
        this.init();
    };
    _pro.init = function(){
        this.bind_event();
        this.init_loop();
        this.auto_scroll();
    };
    _pro.bind_event = function(){
        var self = this;
        self.box[0].parentNode.addEventListener('touchstart',function(e){
            self.__touching = !0;
            self.__touStartTime= +new Date();
            if(e.touches.length==1 && !self.busy){
                self.pointX = e.touches[0].screenX;
                self.pointY = e.touches[0].screenY;
                self.point0 = {x:self.pointX, y:self.pointY };
                self.__action = '';
            }
        });
        self.box[0].parentNode.addEventListener('touchmove',function(e){
            if(e.touches.length==1 && !self.busy){
                if ( self.move(e.touches[0].screenX,e.touches[0].screenY) ){//这里根据返回值是否阻止默认touch事件,左右滑动时需要阻止
                    e.preventDefault();
                }
            }
        });
        self.box[0].parentNode.addEventListener('touchend',function(e){
            self.__touching = !1;
            !self.busy && self.__action==='LR' && self.move_end();
            self.__action = '';
        });
        self.box[0].parentNode.addEventListener('touchcancel',function(e){
            self.__touching = !1;
            self.__action = '';
        });
        var supportsOrientationChange = "onorientationchange" in window,
            orientationEvent = supportsOrientationChange  ? "orientationchange" : "resize";
        window.addEventListener(orientationEvent, function(evt){
            setTimeout(function(){
                self.width = self.box._$children()._$get(0).scrollWidth;
                self.nowLeft = -(self.index||0) * self.width;
                self.box[0].setAttribute('style',self.get_style(2));
                self.minleft = -self.width*(self.size-1);
            }, 200);
        });
    };
    /*
     初始化循环滚动,当一次性需要滚动多个子元素时，暂不支持循环滚动效果,
     如果想实现一次性滚动��个子元素效果，可以通过页面结构实现
     循环滚动思路：复制首尾节点到尾首
     */
    _pro.init_loop = function(){
        if(this.box._$children().length == this.size && this.loop){//暂时只支持size和子节点数相等情况的循环
            this.nowLeft = -this.width;//设置初始位置信息
            this.minleft = -this.width*this.size;//最小left值
            this.maxleft = -this.width;
            this.box._$insert(this.box._$children()._$get(this.size-1,true)._$clone(true), 'top')
                ._$insert(this.box._$children()._$get(1,true)._$clone(true), 'bottom');
            this.box[0].setAttribute('style',this.get_style(2));
// this.box._$style('width',this.width*(this.size+2));
        }else{
            this.loop = false;
// this.box._$style('width',this.width*this.size);
        }
    };
    /**
     * 判断是否需要自动滚动， 在控件没有显示在可见区域时，不自动滚动
     * @return {Bollean} ture 需要滚动， false不需要
     */
    _pro.shouldAutoScroll = (function(){
        function getWinH(){
            var winH;
            if(window.innerHeight) { // all except IE
                winH = window.innerHeight;
            }else if (window.document.body) { // other
                winH = window.document.body.clientHeight;
            }
            return winH || 0;
        };
        function isInViewport(node,_winH){
            var rect = node.getBoundingClientRect();
            if (rect.bottom >= 0 && rect.top <= _winH) {
                return true;
            }
            return false;
        }
        return function(){
            return isInViewport(this.box[0], getWinH());
        }
    })();
    _pro.auto_scroll = function(){//自动滚动
        var self = this;
        if(!self.loop || !self.auto)return;
        clearTimeout(self.timer);
        self.timer = setTimeout(function(){
//仅仅在用户没有手工拖动时自动轮播到下一张
//用户手工拖动时则直接跳过自动轮播，重新设置定时器
            if (self.__touching) {
                self.auto_scroll();
            }else{
                if (self.shouldAutoScroll()) {
                    self.go_index(self.index+1, null, true);
                }else{
                    self.auto_scroll();
                }
            }
        },self.slideInterval);
    };
    _pro.go_index = function(ind, touched, auto){//滚动到指定索引页面
        var self = this;
        if(self.busy)return;
        clearTimeout(self.timer);
        self.busy = true;
        if(self.loop){//如果循环
            ind = ind<0?-1:ind;
            ind = ind>self.size?self.size:ind;
        }else{
            ind = ind<0?0:ind;
            ind = ind>=self.size?(self.size-1):ind;
        }
        if(!self.loop && (self.nowLeft == -(self.width*ind))){
            self.complete(ind);
        }else if(self.loop && (self.nowLeft == -self.width*(ind+1))){
            self.complete(ind);
        }else{
            var fromLeft = self.nowLeft;
            if(ind == -1 || ind == self.size){//循环滚动边界
                self.index = ind==-1?(self.size-1):0;
                self.nowLeft = ind==-1?0:-self.width*(self.size+1);
            }else{
                self.index = ind;
                self.nowLeft = -(self.width*(self.index+(self.loop?1:0)));
            }
            var _newScrollTime = 0;
            if (touched && self.__touStartTime) {
                try{
                    var moveTime = (+new Date())-self.__touStartTime;
                    _newScrollTime = 0.9*Math.abs(fromLeft-self.nowLeft) * moveTime /(self.width - Math.abs(fromLeft-self.nowLeft)+1) ;
                    _newScrollTime = (self.width - Math.abs(fromLeft-self.nowLeft)+1)<30 ? 300 : _newScrollTime;
                    _newScrollTime = _newScrollTime < 150 ? 150 : _newScrollTime;
                    _newScrollTime = _newScrollTime > self.scrollTime*1.5 ? self.scrollTime*1.5 : _newScrollTime;
                }catch(e){
                    _newScrollTime = 0;
                }
            }
            var timingFunc = !!auto ? 'cubic-bezier(.67,.17,.52,.97)':'easeout';
            var _easeout = _ani._$$Timing._$allocate({
                timing: timingFunc,
                from: {
                    offset: fromLeft
                },
                to: {
                    offset: self.nowLeft
                },
                duration: _newScrollTime||self.scrollTime,
                onupdate: function(_evt){
                    self.nowLeft = _evt.offset;
                    self.box[0].setAttribute('style',self.get_style(2));
                },
                onstop: function(){
                    _easeout._$recycle();
                    self.complete(ind);
                }
            });
            _easeout._$play();
        }
    };
    _pro.complete = function(ind){//动画完成回调
        var self = this;
        self.busy = false;
        self.config.callback && self.config.callback(self.index);
        if(ind==-1){
            self.nowLeft = self.minleft;
        }else if(ind==self.size){
            self.nowLeft = self.maxleft;
        }
        self.box[0].setAttribute('style',self.get_style(2));
        self.auto_scroll();
    };
    _pro.next = function(){//下一页滚动
        if(!this.busy){
            this.go_index(this.index+1);
        }
    };
    _pro.prev = function(){//上一页滚动
        if(!this.busy){
            this.go_index(this.index-1);
        }
    };
    _pro.move = function(pointX,pointY){//滑动屏幕处理函数
// this.log('action: '+ this.__action);
        var changeX = pointX - (this.pointX===null?pointX:this.pointX),
            changeY = pointY - (this.pointY===null?pointY:this.pointY),
            marginleft = this.nowLeft, return_value = false;
        if (this.__action==='UD') {
            return false;
        }else{
            return_value = true;
        }
        this.nowLeft = marginleft+changeX;
        this.moveLeft = changeX<0;
        if ( !this.__action ){ //滑动屏幕角度范围：45度
            var dx = Math.abs(pointX - this.point0.x),
                dy = Math.abs(pointY - this.point0.y);
            if (dx>5 || dy>5) {
                if (  dx > dy ) {
                    this.__action = 'LR';
                    return_value = true;
                }else{
                    this.__action = 'UD';
                    return false;
                }
            }else{
//ios safari 如果此时阻止默认行为会导致后续上下滚动存在问题
                return false
            }
        }
        this.pointX = pointX;
        this.pointY = pointY;
        this.box[0].setAttribute('style',this.get_style(2));
        return return_value;
    };
    _pro.move_end = function(){
        var changeX = this.nowLeft%this.width,ind;
        if(this.nowLeft<this.minleft){//手指向左滑动
            ind = this.index +1;
        }else if(this.nowLeft>this.maxleft){//手指向右滑动
            ind = this.index-1;
        }else if(changeX!==0){
            if(this.moveLeft){//手指向左滑动
                ind = this.index+1;
            }else{//手指向右滑动
                ind = this.index-1;
            }
        }else{
            ind = this.index;
        }
        this.pointX = this.pointY = null;
        this.go_index(ind, true);
    };
    /*
     获取动画样式，要兼容更多浏览器，可以扩展该方法
     @int fig : 1 动画 2  没动画
     */
    _pro.get_style = function(fig){
        var x = this.nowLeft ,
            time = fig==1?this.scrollTime:0;
        return '-webkit-transition:'+'-webkit-transform '+time+'ms;'+
            '-webkit-transform:'+'translate3d('+x+'px,0,0);'+
            '-webkit-backface-visibility;'+'hidden;'+
            'transition:'+'transform '+time+'ms ease-out;'+
            'transform:'+'translate3d('+x+'px,0,0);';
    };
    return _p._$$Slider;
},1,2,6,30,114);
I$(330,
	function(_k,   Module, Slider, _q) {
		_k._$$IndexModule = _k._$klass();
		pro = _k._$$IndexModule._$extend(Module);
		pro.__init = function(_options) {
			


			// this.__appendContents();
			if (_q('.m-imgslider-wrap .imgpagebox').length) {
				Slider._$allocate({
					box: _q('.m-imgslider-wrap .m-slide')[0],
					loop: true,
					auto: true,
					scrollTime: 200,
					callback: this._$sliderChange()
				});


			}




		};




		pro._$sliderChange = function() {
			var pageBox = _q('.m-imgslider-wrap .imgpagebox');
			return function(idx) {
				pageBox._$children('.active', true)._$delClassName('active');
				pageBox._$children('.dot', true)._$get(idx, true)._$addClassName('active');


			};


		};


		_k._$$IndexModule._$allocate();


	},
	1,7, 109, 6);

