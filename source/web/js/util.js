;;function yqGetQuery(a){var d=window.location.href;var b=new RegExp("(^|&)"+a+"=([^&]*)(&|$)");var c=d.substr(d.indexOf("?")+1).match(b);if(c!=null){return unescape(c[2])}return null};if (yqGetQuery('device')!='m_mobile' && /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase())) {
window.location.href = "http://m.qqqg.com";};var JSON;if(!JSON){JSON={}}(function(){function f(n){return n<10?"0"+n:n}if(typeof Date.prototype.toJSON!=="function"){Date.prototype.toJSON=function(key){return isFinite(this.valueOf())?this.getUTCFullYear()+"-"+f(this.getUTCMonth()+1)+"-"+f(this.getUTCDate())+"T"+f(this.getUTCHours())+":"+f(this.getUTCMinutes())+":"+f(this.getUTCSeconds())+"Z":null};String.prototype.toJSON=Number.prototype.toJSON=Boolean.prototype.toJSON=function(key){return this.valueOf()}}var cx=/[\u0000\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,escapable=/[\\\"\x00-\x1f\x7f-\x9f\u00ad\u0600-\u0604\u070f\u17b4\u17b5\u200c-\u200f\u2028-\u202f\u2060-\u206f\ufeff\ufff0-\uffff]/g,gap,indent,meta={"\b":"\\b","\t":"\\t","\n":"\\n","\f":"\\f","\r":"\\r",'"':'\\"',"\\":"\\\\"},rep;function quote(string){escapable.lastIndex=0;return escapable.test(string)?'"'+string.replace(escapable,function(a){var c=meta[a];return typeof c==="string"?c:"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)})+'"':'"'+string+'"'}function str(key,holder){var i,k,v,length,mind=gap,partial,value=holder[key];if(value&&typeof value==="object"&&typeof value.toJSON==="function"){value=value.toJSON(key)}if(typeof rep==="function"){value=rep.call(holder,key,value)}switch(typeof value){case"string":return quote(value);case"number":return isFinite(value)?String(value):"null";case"boolean":case"null":return String(value);case"object":if(!value){return"null"}gap+=indent;partial=[];if(Object.prototype.toString.apply(value)==="[object Array]"){length=value.length;for(i=0;i<length;i+=1){partial[i]=str(i,value)||"null"}v=partial.length===0?"[]":gap?"[\n"+gap+partial.join(",\n"+gap)+"\n"+mind+"]":"["+partial.join(",")+"]";gap=mind;return v}if(rep&&typeof rep==="object"){length=rep.length;for(i=0;i<length;i+=1){if(typeof rep[i]==="string"){k=rep[i];v=str(k,value);if(v){partial.push(quote(k)+(gap?": ":":")+v)}}}}else{for(k in value){if(Object.prototype.hasOwnProperty.call(value,k)){v=str(k,value);if(v){partial.push(quote(k)+(gap?": ":":")+v)}}}}v=partial.length===0?"{}":gap?"{\n"+gap+partial.join(",\n"+gap)+"\n"+mind+"}":"{"+partial.join(",")+"}";gap=mind;return v}}if(typeof JSON.stringify!=="function"){JSON.stringify=function(value,replacer,space){var i;gap="";indent="";if(typeof space==="number"){for(i=0;i<space;i+=1){indent+=" "}}else{if(typeof space==="string"){indent=space}}rep=replacer;if(replacer&&typeof replacer!=="function"&&(typeof replacer!=="object"||typeof replacer.length!=="number")){throw new Error("JSON.stringify")}return str("",{"":value})}}if(typeof JSON.parse!=="function"){JSON.parse=function(text,reviver){var j;function walk(holder,key){var k,v,value=holder[key];if(value&&typeof value==="object"){for(k in value){if(Object.prototype.hasOwnProperty.call(value,k)){v=walk(value,k);if(v!==undefined){value[k]=v}else{delete value[k]}}}}return reviver.call(holder,key,value)}text=String(text);cx.lastIndex=0;if(cx.test(text)){text=text.replace(cx,function(a){return"\\u"+("0000"+a.charCodeAt(0).toString(16)).slice(-4)})}if(/^[\],:{}\s]*$/.test(text.replace(/\\(?:["\\\/bfnrt]|u[0-9a-fA-F]{4})/g,"@").replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g,"]").replace(/(?:^|:|,)(?:\s*\[)+/g,""))){j=eval("("+text+")");return typeof reviver==="function"?walk({"":j},""):j}throw new SyntaxError("JSON.parse")}}}());!function(a,b,c,d){var e=a(b);a.fn.lazyload=function(f){function g(){var b=0;i.each(function(){var c=a(this);if(!j.skip_invisible||c.is(":visible"))if(a.abovethetop(this,j)||a.leftofbegin(this,j));else if(a.belowthefold(this,j)||a.rightoffold(this,j)){if(++b>j.failure_limit)return!1}else c.trigger("appear"),b=0})}var h,i=this,j={threshold:0,failure_limit:0,event:"scroll",effect:"show",container:b,data_attribute:"original",skip_invisible:!1,appear:null,load:null,placeholder:"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsQAAA7EAZUrDhsAAAANSURBVBhXYzh8+PB/AAffA0nNPuCLAAAAAElFTkSuQmCC"};return f&&(d!==f.failurelimit&&(f.failure_limit=f.failurelimit,delete f.failurelimit),d!==f.effectspeed&&(f.effect_speed=f.effectspeed,delete f.effectspeed),a.extend(j,f)),h=j.container===d||j.container===b?e:a(j.container),0===j.event.indexOf("scroll")&&h.bind(j.event,function(){return g()}),this.each(function(){var b=this,c=a(b);b.loaded=!1,(c.attr("src")===d||c.attr("src")===!1)&&c.is("img")&&c.attr("src",j.placeholder),c.one("appear",function(){if(!this.loaded){if(j.appear){var d=i.length;j.appear.call(b,d,j)}a("<img />").bind("load",function(){var d=c.attr("data-"+j.data_attribute);c.hide(),c.is("img")?c.attr("src",d):c.css("background-image","url('"+d+"')"),c[j.effect](j.effect_speed),b.loaded=!0;var e=a.grep(i,function(a){return!a.loaded});if(i=a(e),j.load){var f=i.length;j.load.call(b,f,j)}}).attr("src",c.attr("data-"+j.data_attribute))}}),0!==j.event.indexOf("scroll")&&c.bind(j.event,function(){b.loaded||c.trigger("appear")})}),e.bind("resize",function(){g()}),/(?:iphone|ipod|ipad).*os 5/gi.test(navigator.appVersion)&&e.bind("pageshow",function(b){b.originalEvent&&b.originalEvent.persisted&&i.each(function(){a(this).trigger("appear")})}),a(c).ready(function(){g()}),this},a.belowthefold=function(c,f){var g;return g=f.container===d||f.container===b?(b.innerHeight?b.innerHeight:e.height())+e.scrollTop():a(f.container).offset().top+a(f.container).height(),g<=a(c).offset().top-f.threshold},a.rightoffold=function(c,f){var g;return g=f.container===d||f.container===b?e.width()+e.scrollLeft():a(f.container).offset().left+a(f.container).width(),g<=a(c).offset().left-f.threshold},a.abovethetop=function(c,f){var g;return g=f.container===d||f.container===b?e.scrollTop():a(f.container).offset().top,g>=a(c).offset().top+f.threshold+a(c).height()},a.leftofbegin=function(c,f){var g;return g=f.container===d||f.container===b?e.scrollLeft():a(f.container).offset().left,g>=a(c).offset().left+f.threshold+a(c).width()},a.inviewport=function(b,c){return!(a.rightoffold(b,c)||a.leftofbegin(b,c)||a.belowthefold(b,c)||a.abovethetop(b,c))},a.extend(a.expr[":"],{"below-the-fold":function(b){return a.belowthefold(b,{threshold:0})},"above-the-top":function(b){return!a.belowthefold(b,{threshold:0})},"right-of-screen":function(b){return a.rightoffold(b,{threshold:0})},"left-of-screen":function(b){return!a.rightoffold(b,{threshold:0})},"in-viewport":function(b){return a.inviewport(b,{threshold:0})},"above-the-fold":function(b){return!a.belowthefold(b,{threshold:0})},"right-of-fold":function(b){return a.rightoffold(b,{threshold:0})},"left-of-fold":function(b){return!a.rightoffold(b,{threshold:0})}})}(jQuery,window,document);
$.extend({getMyScript:function(a,b,c){if(jQuery.isFunction(b)){c=b;b={}}return jQuery.ajax({type:"get",url:a,data:b,success:c,dataType:"script",cache:true})}});
QTIMES={};QTIMES.date={date_part:function(a){a.setHours(0);a.setMinutes(0);a.setSeconds(0);a.setMilliseconds(0);if(a.getHours()!=0){a.setTime(a.getTime()+60*60*1000*(24-a.getHours()))}return a},time_part:function(a){return(a.valueOf()/1000-a.getTimezoneOffset()*60)%86400},week_start:function(b){var a=b.getDay();if(scheduler.config.start_on_monday){if(a===0){a=6}else{a--}}return this.date_part(this.add(b,-1*a,"day"))},month_start:function(a){a.setDate(1);return this.date_part(a)},year_start:function(a){a.setMonth(0);return this.month_start(a)},day_start:function(a){return this.date_part(a)},add:function(b,c,d){var a=new Date(b.valueOf());switch(d){case"week":c*=7;case"day":a.setDate(a.getDate()+c);if(!b.getHours()&&a.getHours()){a.setTime(a.getTime()+60*60*1000*(24-a.getHours()))}break;case"month":a.setMonth(a.getMonth()+c);break;case"year":a.setYear(a.getFullYear()+c);break;case"hour":a.setHours(a.getHours()+c);break;case"minute":a.setMinutes(a.getMinutes()+c);break;default:return scheduler.date["add_"+d](b,c,d)}return a},to_fixed:function(a){if(a<10){return"0"+a}return a},copy:function(a){return new Date(a.valueOf())},date_to_str:function(b,a){b=b.replace(/%[a-zA-Z]/g,function(c){switch(c){case"%d":return'"+QTIMES.date.to_fixed(date.getDate())+"';case"%m":return'"+QTIMES.date.to_fixed((date.getMonth()+1))+"';case"%j":return'"+date.getDate()+"';case"%n":return'"+(date.getMonth()+1)+"';case"%y":return'"+QTIMES.date.to_fixed(date.getFullYear()%100)+"';case"%Y":return'"+date.getFullYear()+"';case"%D":return'"+QTIMES.locale.date.day_short[date.getDay()]+"';case"%l":return'"+QTIMES.locale.date.day_full[date.getDay()]+"';case"%M":return'"+QTIMES.locale.date.month_short[date.getMonth()]+"';case"%F":return'"+QTIMES.locale.date.month_full[date.getMonth()]+"';case"%h":return'"+QTIMES.date.to_fixed((date.getHours()+11)%12+1)+"';case"%g":return'"+((date.getHours()+11)%12+1)+"';case"%G":return'"+date.getHours()+"';case"%H":return'"+QTIMES.date.to_fixed(date.getHours())+"';case"%i":return'"+QTIMES.date.to_fixed(date.getMinutes())+"';case"%a":return'"+(date.getHours()>11?"pm":"am")+"';case"%A":return'"+(date.getHours()>11?"PM":"AM")+"';case"%s":return'"+QTIMES.date.to_fixed(date.getSeconds())+"';case"%W":return'"+QTIMES.date.to_fixed(QTIMES.date.getISOWeek(date))+"';default:return c}});if(a){b=b.replace(/date\.get/g,"date.getUTC")}return new Function("date",'return "'+b+'";')},str_to_date:function(f,c){var e="var temp=date.match(/[a-zA-Z]+|[0-9]+/g);";var a=f.match(/%[a-zA-Z]/g);for(var b=0;b<a.length;b++){switch(a[b]){case"%j":case"%d":e+="set[2]=temp["+b+"]||1;";break;case"%n":case"%m":e+="set[1]=(temp["+b+"]||1)-1;";break;case"%y":e+="set[0]=temp["+b+"]*1+(temp["+b+"]>50?1900:2000);";break;case"%g":case"%G":case"%h":case"%H":e+="set[3]=temp["+b+"]||0;";break;case"%i":e+="set[4]=temp["+b+"]||0;";break;case"%Y":e+="set[0]=temp["+b+"]||0;";break;case"%a":case"%A":e+="set[3]=set[3]%12+((temp["+b+"]||'').toLowerCase()=='am'?0:12);";break;case"%s":e+="set[5]=temp["+b+"]||0;";break;case"%M":e+="set[1]=scheduler.locale.date.month_short_hash[temp["+b+"]]||0;";break;case"%F":e+="set[1]=scheduler.locale.date.month_full_hash[temp["+b+"]]||0;";break;default:break}}var d="set[0],set[1],set[2],set[3],set[4],set[5]";if(c){d=" Date.UTC("+d+")"}return new Function("date","var set=[0,0,1,0,0,0]; "+e+" return new Date("+d+");")},getISOWeek:function(c){if(!c){return false}var b=c.getDay();if(b===0){b=7}var d=new Date(c.valueOf());d.setDate(c.getDate()+(4-b));var e=d.getFullYear();var f=Math.round((d.getTime()-new Date(e,0,1).getTime())/86400000);var a=1+Math.floor(f/7);return a},getUTCISOWeek:function(a){return this.getISOWeek(this.convert_to_utc(a))},convert_to_utc:function(a){return new Date(a.getUTCFullYear(),a.getUTCMonth(),a.getUTCDate(),a.getUTCHours(),a.getUTCMinutes(),a.getUTCSeconds())}};QTIMES.locale={date:{month_full:["January","February","March","April","May","June","July","August","September","October","November","December"],month_short:["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"],day_full:["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],day_short:["Sun","Mon","Tue","Wed","Thu","Fri","Sat"]}};
;;(function( window, undefined ) {
    ht={};
    ht.util={
        init:function(){
            this.searchBanner.init();
            this.alpha();
            this.lazyLoadPhoto.init();
            this.siderStickySearch.init();
            this.nav.init();
            this.catalog.init();
            this.loginDialog.init();
            this.login.init();
            this.shopcarts.init();
            this.catagroy.init();
        },
        checkPictureType:function(fileName){
            var acceptFileTypes= /\.(gif|jpe?g|png)$/i
            if( acceptFileTypes.test(fileName) )
            {
                return 1;
            }
            else
            {
                return 0;
            }
        },
        ops:{
            //不同保税仓的上税规则
            tax:[
                {id:0,taxRate:50,maxPrice:1000,txt:'国外',payTax:1},
                {id:1,taxRate:0,maxPrice:0,txt:'国内',payTax:0}
            ]
        },
        catagroy:{
            init:function(){
                if($('#funcTab')[0]){
                    this.bindEvent();
                    this.get();
                }
            },
            bindEvent:function(){
                $('#funcTab .item').hover(function(){
                    $(this).addClass('navhover');
                },function(){
                    $(this).removeClass('navhover');
                })
            },
            parseData:function(data){
                var data= data;
                var hashData = {};
                for(var i= 0,len=data.length;i<len;i++){
                    for(var m= 0,mLen=data[i].categorys.length;m<mLen;m++){
                        data[i].categorys[m].sons=[];
                    }
                }
                return data;
            },
            get:function(){
                $.get('/item/nav.html',function(r){
                    r=JSON.parse(r);
                    if(r.state==200){
                        var hashData = {};
                        var data=ht.util.catagroy.parseData(r.categorys);

                        for(var i= 0,len=data.length;i<len;i++){
                            for(var m= 0,mLen=data[i].categorys.length;m<mLen;m++){
                                for(var n=0;n<data[i].categorys[m].attributes.length;n++){
                                    if(data[i].categorys[m].attributes[n].value){
                                        for(var u=0;u<data[i].categorys[m].attributes[n].value.length;u++){
                                            data[i].categorys[m].attributes[n].value[u].attribute_id=data[i].categorys[m].attributes[n].attribute_id;
                                            data[i].categorys[m].attributes[n].value[u].show_id=data[i].categorys[m].show_id;

                                            data[i].categorys[m].sons.push(data[i].categorys[m].attributes[n].value[u]);


                                        }
                                    }

                                }
                            }

                            hashData[data[i].top_category_id]=data[i].categorys;
                        }

                        $('#funcTab .item[data-cate-id]').each(function(){
                            var cateID=$(this).attr('data-cate-id');

                            if(hashData[cateID].length>0){
                                $(this).append('<div class="m-ctgcard f-cb"><div class="f-fl m-ctglist"><div class="m-ctgtbl"></div></div></div>');
                                $('#templateCates').tmpl(hashData[cateID]).appendTo($(this).find('.m-ctgtbl'));
                            }

                        });

                    }

                });
            }
        },
        checkPictureType:function(fileName){
            var acceptFileTypes= /\.(gif|jpe?g|png)$/i;
            return acceptFileTypes.test(fileName);
        },
        getQuery:function(name){
            var myLocation=window.location.href;
            var reg = new RegExp("(^|&)"+ name +"=([^&]*)(&|$)");
            var r = myLocation.substr(myLocation.indexOf("\?")+1).match(reg);
            if (r!=null) return unescape(r[2]); return null;
        },
        cookies:{
            // write cookies
            set:function(name, value, hours,domain){
                var expire = "";
                if(hours != null)
                {
                    expire = new Date((new Date()).getTime() + hours * 3600000);
                    expire = "; expires=" + expire.toGMTString();
                }
                var str=name + "=" + escape(value) + expire+";path=/";
                if(domain) str+='; domain='+domain;
                document.cookie = str;
            },
            // read cookies
            get:function(name){
                var cookieValue = "";
                var search = name + "=";
                if(document.cookie.length > 0)
                {
                    offset = document.cookie.indexOf(search);
                    if (offset != -1)
                    {
                        offset += search.length;
                        end = document.cookie.indexOf(";", offset);
                        if (end == -1) end = document.cookie.length;
                        cookieValue = unescape(document.cookie.substring(offset, end))
                    }
                }
                return cookieValue;
            }
        },
        alpha:function(){
            $('#rightBar2 .m-app2').remove();
        },
        lazyLoadPhoto:{
            init:function(){
                $("img.img-lazyload").lazyload();
            }
        },
        siderStickySearch:{
            init:function(){
                if($('#banner-box')[0]){
                    ht.util.slider.init();
                    ht.util.stickySearch();
                }

            }
        },
        searchBanner:{
            init:function(){
                this.bindEvent();
            },
            bindEvent:function(){
                $('#htHeader').on('click','.itemVal',function(){
                    window.open('/search.html?key='+escape($(this).text()));
                });
            }
        },
        stickySearch:function(){
            var $hearder=$('#topTabBox');
            if(!$hearder[0]){
                return;
            }
            var top=$hearder.offset().top;
            $(window).on("scroll", function () {
                var s=$(window).scrollTop();
                s > top ? $hearder.addClass('topTabBoxFixed') : $hearder.removeClass('topTabBoxFixed');
            });
        },
        shopcarts:{
            init:function(){
                this.cartproducts();
            },
            cartproducts:function(){
                $('.shopcart').click(function(){
                    $(this).closest('form')[0].submit();
                    return false;
                });
            }
        },
        validformParam:{
            datatype: {
                "*6-20": /^[^\s]{6,20}$/,
                "z2-9": /^[\u4E00-\u9FA5\uf900-\ufa2d]{2,9}$/,
                "phone": /^1\d{10}$/,
                "local":function(){
                    var isOk=true;
                    $('#provicecityarea .ellipsis').each(function(){
                        if($('#provicecityarea .ellipsis').attr('value')==''){
                            isOk=false;
                        }
                    });
                    return isOk;
                },
                "idcard": function (gets,obj,curform,datatype) {
                    var Wi = [ 7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1 ];// 加权因子;
                    var ValideCode = [ 1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2 ];// 身份证验证位值，10代表X;

                    if (gets.length == 15) {
                        return isValidityBrithBy15IdCard(gets);
                    }else if (gets.length == 18){
                        var a_idCard = gets.split("");// 得到身份证数组
                        if (isValidityBrithBy18IdCard(gets)&&isTrueValidateCodeBy18IdCard(a_idCard)) {
                            return true;
                        }
                        return false;
                    }
                    return false;

                    function isTrueValidateCodeBy18IdCard(a_idCard) {
                        var sum = 0; // 声明加权求和变量
                        if (a_idCard[17].toLowerCase() == 'x') {
                            a_idCard[17] = 10;// 将最后位为x的验证码替换为10方便后续操作
                        }
                        for ( var i = 0; i < 17; i++) {
                            sum += Wi[i] * a_idCard[i];// 加权求和
                        }
                        valCodePosition = sum % 11;// 得到验证码所位置
                        if (a_idCard[17] == ValideCode[valCodePosition]) {
                            return true;
                        }
                        return false;
                    }

                    function isValidityBrithBy18IdCard(idCard18){
                        var year = idCard18.substring(6,10);
                        var month = idCard18.substring(10,12);
                        var day = idCard18.substring(12,14);
                        var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));
                        // 这里用getFullYear()获取年份，避免千年虫问题
                        if(temp_date.getFullYear()!=parseFloat(year) || temp_date.getMonth()!=parseFloat(month)-1 || temp_date.getDate()!=parseFloat(day)){
                            return false;
                        }
                        return true;
                    }

                    function isValidityBrithBy15IdCard(idCard15){
                        var year =  idCard15.substring(6,8);
                        var month = idCard15.substring(8,10);
                        var day = idCard15.substring(10,12);
                        var temp_date = new Date(year,parseFloat(month)-1,parseFloat(day));
                        // 对于老身份证中的你年龄则不需考虑千年虫问题而使用getYear()方法
                        if(temp_date.getYear()!=parseFloat(year) || temp_date.getMonth()!=parseFloat(month)-1 || temp_date.getDate()!=parseFloat(day)){
                            return false;
                        }
                        return true;
                    }


                }
            }
        },
        location:{
            init:function(){
                this.getLocation();
                this.bindEvent();
            },
            locationClass:[
                'zp-province',
                'zp-city',
                'zp-district'
            ],
            locationTxt:[
                '--省/直辖市--',
                '--市--',
                '--县/区--'
            ],
            getLocation:function(){
                $("#locationValue").append('<input type="hidden" id="myLocation" name="myLocation"  autocomplete="off" datatype="*" nullmsg="请选择省市区！" errormsg="请选择省市区"  />');
                var str='<input type="hidden" id="province" name="province"  autocomplete="off"  />';
                str+='<input type="hidden" id="city" name="city"  autocomplete="off"   />';
                str+='<input type="hidden" id="area" name="area"  autocomplete="off"   />';
                $("#locationValue").append(str);

                this.get(null,this.locationClass[0],0);

            },
            get:function(param,className,index,callback){
                var _this=this;
                $.get('/common/location.html',param,function(r){
                    var r=JSON.parse(r);
                    r.zClass=className;
                    r.locationTxt=_this.locationTxt[index];

                    $( "#templateLocation" ).tmpl( r )
                        .appendTo( "#provicecityarea" );

                    callback && callback();
                });
            },
            bindEvent:function(){
                var _this=this;
                $(document).click(function(e){
                    var target  = $(e.target);
                    if(target.closest(".nselect-wrap").length == 0 ){
                        $('.options').hide();
                        $(this).find('.cp-arrow').removeClass('cp-arrow-up').addClass('cp-arrow-down');
                    }
                });
                $('body').on('click','.nselect-wrap',function(){
                    if($(this).find('.cp-arrow').hasClass('cp-arrow-down')){
                        var index=$(this).index();
                        $('.cp-arrow').removeClass('cp-arrow-up').addClass('cp-arrow-down');
                        $(this).find('.cp-arrow').removeClass('cp-arrow-down').addClass('cp-arrow-up');
                        $(this).find('.options-wrap').find('.options').show();
                        $('.options').not($(this).find('.options')).hide();
                    }else{
                        $(this).find('.cp-arrow').removeClass('cp-arrow-up').addClass('cp-arrow-down');
                        $(this).find('.options-wrap').find('.options').hide();
                        $('.options').not($(this).find('.options')).hide();

                    }
                });
                $('body').on('click','.option',function(){
                    var $ancestors=$(this).closest('.nselector');
                    $ancestors.find('.curr').removeClass('curr');
                    var txt=$(this).html();
                    var val=$(this).attr('value');
                    $(this).addClass('curr').closest('.nselector').find('.result').html(txt).attr('value',val);
                    var $root=$(this).closest('.nselect-wrap');
                    var index=$('.nselect-wrap').index($root);
                    $('.nselect-wrap:gt('+index+')').remove();

                    var cName=_this.locationClass[index+1];
                    var param={
                        parent_id:val
                    }
                    if(index==0){
                        param.query_type='city';
                        $('#myLocation').val('');
                    }else if(index==1){
                        param.query_type='area';
                        $('#myLocation').val('');
                    }else{
                        $('#myLocation').val('1');
                        return;
                    }
                    var txtIndex=index+1;

                    ht.util.location.get(param,cName,txtIndex);
                });

            }

        },
        nav:{
            init:function(){
                this.bindEvent();
            },
            bindEvent:function(){
                var _this=this;
                _this.navDrop();
                $('#addFavBtn').click(function(){
                    _this.addFav('全球抢购 正品保正','http://www.qqqg.com/')
                });
            },
            navDrop:function(){
                $('.mcDropMenuBox').hover(function(){
                    $(this).addClass('mcDropMenuBoxActive');
                },function(){
                    $(this).removeClass('mcDropMenuBoxActive');
                });
            },
            addFav: function (title, url) {
                try {
                    window.external.addFavorite(url, title);
                }
                catch (e) {
                    try {
                        window.sidebar.addPanel(title, url, "");
                    }
                    catch (e) {
                        window.alert("请尝试点击 Ctrl + D 来添加！")
                    }
                }
            }
        },
        sticky:function($obj,callbackFixed,callback){
            var top=$obj.offset().top;
            $(window).on("scroll", function () {
                var s=$(window).scrollTop();
                s > top ? callbackFixed() : callback();
            });
        },
        lazyGet:function($obj,callback,h){
            function getClient(){
                var l, t, w, h;
                l = document.documentElement.scrollLeft || document.body.scrollLeft;
                t = document.documentElement.scrollTop || document.body.scrollTop;
                w = document.documentElement.clientWidth;
                h = document.documentElement.clientHeight;
                return { left: l, top: t, width: w, height: h };
            }
            function getSubClient(p){
                var l = 0, t = 0, w, h;
                w = p.offsetWidth;
                h = p.offsetHeight;
                while(p.offsetParent){
                    l += p.offsetLeft;
                    t += p.offsetTop;
                    p = p.offsetParent;
                }
                return { left: l, top: t, width: w, height: h };
            }
            function intens(rec1, rec2){
                var lc1, lc2, tc1, tc2, w1, h1;
                lc1 = rec1.left + rec1.width / 2;
                lc2 = rec2.left + rec2.width / 2;
                tc1 = rec1.top + rec1.height / 2 ;
                tc2 = rec2.top + rec2.height / 2 ;
                w1 = (rec1.width + rec2.width) / 2 ;
                h1 = (rec1.height + rec2.height) / 2;
                return Math.abs(lc1 - lc2) < w1 && Math.abs(tc1 - tc2) < h1 ;
            }
            function areaCheck(){
                if($obj.hasClass('isLoaded')){return}
                var div1 = $obj[0];
                var prec1 = getClient();
                var prec2 = getSubClient(div1);
                if (intens(prec1, prec2)) {
                    callback();
                    $obj.addClass('isLoaded');
                    return;
                }
            }
            areaCheck();
            window.onscroll = function(){
                areaCheck();
            };
            window.onresize = function(){
                areaCheck();
            }
        },
        shopcartFix:{
            init:function(){
                ht.util.sticky($('#rightBar2'),function(){
                    $('#rightBar2').css({'position':'fixed','top':'66'});
                },function(){
                    $('#rightBar2').css({'position':'fixed','top':'283'});
                });
            }
        },
        placeholder:function(){
            //判断浏览器是否支持placeholder属性
            supportPlaceholder='placeholder'in document.createElement('input');
            //当浏览器不支持placeholder属性时，调用placeholder函数
            if(!supportPlaceholder){
                $('[placeholder]').each(function(){
                    $(this).after('<span class="inputTip">'+$(this).attr("placeholder")+'</span>');
                });
                // $('[placeholder]').after('<span class="inputTip">'+$(this).attr("placeholder")+'</span>');

                $('[placeholder]').keydown(function(){
                    $(this).next('.inputTip').remove();
                }).focus(function(){

                }).blur(function(){
                    if ($(this).val() == '') {
                        $(this).after('<span class="inputTip">'+$(this).attr("placeholder")+'</span>');
                    }
                });
            }
        },
        getImgCode:function(){
            return '/common/image_code/?'+Math.random();
        },
        ex:{
            email: /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,
            mobile: /^1\d{10}$/,
            digital: /\d+/,
            lowercase: /[a-z]+/,
            uppercase: /[A-Z]+/,
            symbols: /[_!@#\$%\^&\*\(\)\\\|\/\?\.\<\>'"\{\}\[\]=\-\~\,\;\:\s]+/,
            password: /^[a-zA-Z0-9_!@#\$%\^&\*\(\)\\\|\/\?\.\<\>'"\{\}\[\]=\-\~\,\;\:\s]+$/,
            mobile_verify: /^\d{6}$/
        },
        popAlert:{
            setOps:function(){
                $.blockUI.defaults.css.border='2px solid #ccc';
                $.blockUI.defaults.css.cursor='cursor';
                $.blockUI.defaults.overlayCSS.opacity=0.3;
                $.blockUI.defaults.overlayCSS.cursor='cursor';
            },
            run:function(callback) {
                var _this=this;
                $.getMyScript('http://cdn.qqqg.com/web/js/plugin/jquery.blockui.js', function () {
                    _this.setOps();
                    callback();
                    $('.blockUI').on('click','.iDialogClose,.iDialogNo',function(){
                        $.unblockUI();
                    });
                });
            },
            popHtml:function(str,dialogId,isConfirm,title){
                var confirmHtml="<a class=\"iDialogBtn focusBtn iDialogYes\" rel=\"1\" href=\"javascript:;\"><span>确认</span></a><a class=\"iDialogBtn iDialogNo\" rel=\"0\" href=\"javascript:;\"><span>取消</span></a>";
                if(!isConfirm){
                    confirmHtml='';
                }
                var strTitle=title?title:'提示';
                var reval  = "";
                reval += "<div id=\""+dialogId+"\">";
                reval += "    <div class=\"iDialogHead\">";
                reval += "        <h1>"+strTitle+"</h1>";
                reval += "    </div>";
                reval += "    <a href=\"#\" hidefocus=\"true\" class=\"iDialogClose\">×</a>";
                reval += "    <div class=\"iDialogBody\">";
                reval += "        <div class=\"iDialogMain\">";
                reval += "            <div class=\"staDialogStyle\" style=\"padding-right: 53px;\"><i class=\"alert\"></i>"+str+"</div>";
                reval += "        </div>";
                reval += "    </div>";
                reval += "    <div class=\"iDialogFoot\">"+confirmHtml;
                reval += "    </div>";
                reval += "</div>";
                return reval;
            },
            confirm:function(str,dialogId,title){
                var reval  = "";
                reval=this.popHtml(str,dialogId,1,title);
                return reval;
            },
            loading:function(callback){
                var _this=this;
                $.getMyScript('http://cdn.qqqg.com/web/js/plugin/jquery.blockui.js', function () {
                    $.blockUI(
                        {
                            css: {
                                border: 'none',
                                backgroundColor:'none',
                                top:  ($(window).height() - 100) /2 + 'px',
                                left: ($(window).width() - 100) /2 + 'px',
                                width: '100px'
                            } ,
                            overlayCSS:{
                                backgroundColor:'#000',
                                opacity:.3
                            },
                            message: '<img src="http://cdn.qqqg.com/web/images/loading42.gif" />'
                        }
                    );
                    callback && callback();

                });
            },
            alert:function(str,dialogId){
                var reval  = "";
                reval=this.popHtml(str,dialogId,0);
                return reval;
            }
        },
        dialog:{
            show:function(width,height,html){
                var marginleft=width/2;
                var marginheight=height/2;
                if(!$('#dialog')[0]){
                    $('body').append('<div class="ui-mask-dialog"></div><div id="dialog" class="ui-dialog" style="margin-left: '+marginleft+'px;margin-top: '+marginheight+'px"><div class="dialog-header">提示</div>'+html+'<a class="ui-dialog-close" href="javascript:;">×</a></div>');
                }
                $('#dialog').show();
                $('.ui-mask-dialog').show();
            },
            remove:function(){
                $('#dialog').remove();
                $('.ui-mask-dialog').remove();
            }
        },
        setCountDown:function($obj,str){
            var m=parseInt($obj.attr('v'),10);
            var n=m-1;
            if (n>0) {
                $obj.html('重新获取('+n+')').attr('v',n).addClass("btn_enabled");
                var timeout=setTimeout(function(){
                    ht.util.setCountDown($obj,str);
                },1000);
            } else {
                clearTimeout(timeout);
                $obj.html(str).removeClass("btn_enabled");
            }
        },
        loginDialog:{
            init:function(){
                this.getMask();
                this.getLoginDialog();
                this.bindEvent();
            },
            getMask:function(){
                if(!$('.ui-mask')[0]){
                    $('body').append('<div class="ui-mask"></div>');
                }
            },
            getLoginDialog:function(){
                !$('#login-dialog')[0] && $('body').append(ht.util.loginDialog.getDom());
            },
            bindEvent:function(){
                $('.ui-mask').click(function(){
                    $('.ui-dialog-close').click();
                });
                $('.login').click(function(){
                    $('.ui-mask').show();
                    $('#login-dialog').show();
                    $('#account-dialog').focus();
                });
                $('.ui-dialog-close').click(function(){
                    $('#login-dialog .ui-dialog-container').html(ht.util.loginDialog.getDomInner());
                    $('.ui-mask').hide();
                    $('#login-dialog').hide();
                });
                $('#captcha').click(function(){
                    $(this)[0].src=ht.util.getImgCode();
                });
                $('#changeCaptcha').click(function(){
                    $('#captcha')[0].src=ht.util.getImgCode();
                });

                $('#login_dialog_tab-phone').click(function(){
                    $('#login-form-sms').fadeOut('300',function(){
                        $('#login-form').fadeIn('300');
                    });
                });
                $('#login_dialog_tab-sms').click(function(){
                    $('#login-form').fadeOut('300',function(){
                        $('#login-form-sms').fadeIn('300');
                    });
                });

                $('#login-dialog-getkey').click(function(){
                    var $smsphone=$('#account-dialog-sms');
                    var isSmsphone=ht.util.login.validate.chkAccount($smsphone,$('#login-form-sms'));
                    if(!isSmsphone){
                        return false;
                    }
                    if($(this).hasClass('btn_enabled')) {
                        return false;
                    }
                    var param={
                        phone:$('#account-dialog-sms').val()
                    }
                    var timeline=60;
                    $('#login-dialog-getkey').html('重新获取('+timeline+')').attr('v',timeline).addClass("btn_enabled");
                    $.get('/common/phone/code/',param,function(){
                        ht.util.setCountDown($('#login-dialog-getkey'),'获取动态密码');
                    });
                });

                $('#login-dialog .m-thirdpart').hover(function(){
                    $('#login-dialog-wait').show();
                },function(){
                    $('#login-dialog-wait').hide();
                });
            },
            getDomInner:function(){
                var reval='';
                reval  = "";
                reval += "         <form class=\"login-form\" id=\"login-form\" action=\"\" method=\"post\">";
                reval += "             <div class=\"ui-form\">";
                reval += "                 <div class=\"ui-form-title\">";
                reval += "                     登录";
                reval += "                     <span class=\"logoName\">全球抢购</span>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row\">";
                reval += "                     <span class=\"err\">errText</span>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row\">";
                reval += "                     <input type=\"text\" autocomplete=\"off\" class=\"form-control\" name=\"account\" placeholder=\"手机号码\" maxlength=\"11\" autofocus=\"\" id=\"account-dialog\" />";
                reval += "                     <i class=\"icon-user\"></i>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row\">";
                reval += "                     <input type=\"password\" autocomplete=\"off\" class=\"form-control\" name=\"password\" placeholder=\"密码\" id=\"password-dialog\" />";

                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row row-captcha\">";
                reval += "                     <input type=\"text\" class=\"form-control\" name=\"captcha\" maxlength=\"5\" placeholder=\"验证码\" data-rule=\"验证码必须为5个字符\" id=\"captcha-dialog\" />";
                reval += "                     <a href=\"javascript:;\" rel=\"reload-captcha\"> <img src=\"http://cdn.qqqg.com/web/images/blank.gif\" class=\"captcha\" id=\"captcha\" alt=\"看不清？点击是刷新\" /> </a>";
                reval += "                     <a href=\"javascript:;\" rel=\"reload-captcha\" id=\"changeCaptcha\">换一张</a>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row row-btn\">";
                reval += "                     <input type=\"button\" class=\"btn-primary\" value=\"登录\" data-click-sc=\"login_button_on_dialog\" id=\"loginBtnByPhone\" />";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row forget \">";
                reval += "                     <a class=\"login_dialog_tab\" id=\"login_dialog_tab-sms\" href=\"javascript:void(0);\">短信快捷登录</a>";
                reval += "                     <a class=\"\" href=\"/reg.html\">注册</a>";
                reval += "                     <a href=\"/getpwd.html\">忘记密码？</a>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row thirdpart \">";
                /*
                reval += "                     <ul class=\"m-thirdpart clearfix\">";
                reval += "                         <li class=\"zfb\"> <a href=\"#\" class=\"w-btn3\"> <i class=\"w-icon w-icon-18 w-icon-18-2\"></i><span>支付宝登录</span> </a> </li>";
                reval += "                         <li class=\"wb\"> <a href=\"#\" class=\"w-btn3\"> <i class=\"w-icon w-icon-18\"></i><span>微博登录</span> </a> </li>";
                reval += "                         <li class=\"qq\"> <a href=\"#\" class=\"w-btn3\"> <i class=\"w-icon w-icon-18 w-icon-18-1\"></i><span>QQ登录</span> </a> </li>";
                reval += "                     </ul>";
                */
                reval += "                 </div>";
                reval += "             </div>";
                reval += "         </form>";
                reval += "         <form class=\"login-form\" id=\"login-form-sms\" action=\"\" method=\"post\" style=\"display: none;\">";
                reval += "             <div class=\"ui-form\">";
                reval += "                 <div class=\"ui-form-title\">";
                reval += "                     登录";
                reval += "                     <span class=\"logoName\">全球抢购</span>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row\">";
                reval += "                     <span class=\"err\">errText</span>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row\">";
                reval += "                     <input type=\"text\" autocomplete=\"off\" class=\"form-control\" name=\"account\" placeholder=\"手机号码\" maxlength=\"11\" autofocus=\"\" id=\"account-dialog-sms\" />";
                reval += "                     <i class=\"icon-user\"></i>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row\">";
                reval += "                     <input type=\"password\" autocomplete=\"off\" maxlength=\"4\" class=\"form-control\" name=\"password\" placeholder=\"动态密码\" id=\"keyword-dialog-sms\" />";
                reval += "                    <a id=\"login-dialog-getkey\" class=\"btnMin\">获取动态密码</a>";
                reval += "                 </div>";

                reval += "                 <div class=\"ui-form-row row-btn\">";
                reval += "                     <input type=\"button\" class=\"btn-primary\" value=\"登录\" data-click-sc=\"login_button_on_dialog\" id=\"loginBtnBySms-dialog\" />";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row forget \">";
                reval += "                     <a class=\"login_dialog_tab\" id=\"login_dialog_tab-phone\" href=\"javascript:void(0);\">手机号登录</a>";
                reval += "                     <a class=\"\" href=\"reg.html\">注册</a>";
                reval += "                     <a href=\"/getpwd.html\">忘记密码？</a>";
                reval += "                 </div>";
                reval += "                 <div class=\"ui-form-row thirdpart \">";
                reval += "                     <ul class=\"m-thirdpart clearfix\">";
                reval += "                         <li class=\"zfb\"> <a href=\"#\" class=\"w-btn3\"> <i class=\"w-icon w-icon-18 w-icon-18-2\"></i><span>支付宝登录</span> </a> </li>";
                reval += "                         <li class=\"wb\"> <a href=\"#\" class=\"w-btn3\"> <i class=\"w-icon w-icon-18\"></i><span>微博登录</span> </a> </li>";
                reval += "                         <li class=\"qq\"> <a href=\"#\" class=\"w-btn3\"> <i class=\"w-icon w-icon-18 w-icon-18-1\"></i><span>QQ登录</span> </a> </li>";
                reval += "                     </ul>";
                reval += "                 </div>";
                reval += "             </div>";
                reval += "         </form>";
                reval +='<div id="login-dialog-wait">敬请期待...</div>'
                var loginDialogInner=reval;
                return loginDialogInner;
            },
            getDom:function(){
                var reval  = "";
                reval += "<div id=\"login-dialog\" class=\"ui-dialog login-dialog\">";
                reval += "    <div class=\"ui-dialog-container\">";
                reval += this.getDomInner();
                reval += "    </div>";
                reval += "    <a href=\"javascript:;\" class=\"ui-dialog-close\">×</a>";
                reval += "</div>";
                return reval;
            }
        },
        login:{
            init:function(){
                this.bindEvent();
            },
            labelErr:{
                show:function(str,$parent){
                    var $errObj=$parent.find('.err');
                    $errObj.html(str).show();
                },
                hide:function($parent){
                    var $errObj=$parent.find('.err');
                    $errObj.html('').hide();
                }
            },
            getNext:function(){
                var next=ht.util.getQuery('next');
                return next?next:'/';
            },
            validate:{
                chkAccount:function($obj,$parent){
                    var isOk=false;
                    var $account=$obj;
                    var accountVal=$account.val();


                    if(accountVal==''){
                        ht.util.login.labelErr.show('请输入电话号码',$parent);
                        $account.removeClass('err_label').addClass('err_label');
                    }else if(!ht.util.ex.mobile.test(accountVal)){
                        ht.util.login.labelErr.show('请输入正确格式的手机号码',$parent);
                        $account.removeClass('err_label').addClass('err_label');
                    }else{
                        ht.util.login.labelErr.hide($parent);
                        $account.removeClass('err_label');
                        isOk=true;
                    }
                    return isOk;
                },
                chkPassword:function($parent){
                    var isOk=false;
                    var $password=$('#password-dialog');
                    var passwordVal=$password.val();
                    if(passwordVal==''){
                        ht.util.login.labelErr.show('请输入密码',$parent);
                        $password.removeClass('err_label').addClass('err_label');
                    }else{
                        ht.util.login.labelErr.hide($parent);
                        $password.removeClass('err_label');
                        isOk=true;
                    }
                    return isOk;
                },
                chkCaptcha:function($parent){
                    return true;
                    var isOk=false;
                    var $captcha=$('#captcha-dialog');
                    var captchadVal=$captcha.val();
                    if(captchadVal==''){
                        ht.util.login.labelErr.show('请输入图片验证码',$parent);
                        $captcha.removeClass('err_label').addClass('err_label');
                    }else{
                        ht.util.login.labelErr.hide($parent);
                        $captcha.removeClass('err_label');
                        isOk=true;
                    }
                    isOk=true;
                    return isOk;
                },
                chkSmskeyword:function($parent){
                    var isOk=false;
                    var $obj=$('#keyword-dialog-sms');
                    if($obj.val().length!=4){
                        ht.util.login.labelErr.show('请输入动态密码',$parent);
                        $obj.removeClass('err_label').addClass('err_label');
                    }else{
                        ht.util.login.labelErr.hide($parent);
                        $obj.removeClass('err_label');
                        isOk=true;
                    }
                    return isOk;
                }
            },
            bindEvent:function(){
                $('#topNavWrap').on('click','#loginout',function(){
                    ht.util.cookies.set('loginuser','',-10,'.qqqg.com');
                    ht.util.cookies.set('loginuser','',-10);
                    var url=window.location.href;
                    if(url.indexOf('#')>-1){
                        url=url.replace(/#/g,'');
                    }
                    window.location.href=url;
                });
                $('#password-dialog').keyup(function(e){
                    if(e.keyCode==13){
                        $('#loginBtnByPhone').click();
                    }
                });
                $('#keyword-dialog-sms').keyup(function(e){
                    if(e.keyCode==13){
                        $('#loginBtnBySms-dialog').click();
                    }
                });

                $("#login-dialog").on("click",'#loginBtnByPhone', function(){
                    var isValidAccount=ht.util.login.validate.chkAccount($('#account-dialog'),$('#login-form'));
                    if(!isValidAccount) {
                        return false
                    }
                    var isValidPassword=ht.util.login.validate.chkPassword($('#login-form'));
                    if(!isValidPassword) {
                        return false
                    }
                    var isValidCaptcha=ht.util.login.validate.chkCaptcha($('#login-form'));
                    if(!isValidCaptcha) {
                        return false
                    }
                    if(isValidAccount && isValidPassword && isValidCaptcha){
                        var param={
                            login_type:'usename',
                            usename: $('#account-dialog').val(),
                            password :$('#password-dialog').val(),
                            _xsrf:$('input[name=_xsrf]').val()
                        }
                        $.post('/login.html',param,function(r){
                            var r=JSON.parse(r);
                            if(r.state!=200){
                                ht.util.login.labelErr.show(r.info,$('#login-form'));
                                return false;
                            }else{
                                if($('#toTelRegister')[0]){
                                    window.location.href=ht.util.login.getNext();
                                    return false;
                                }
                                if($('#js_skuBox').attr('needCollect')==1){
                                    $('#js_skuBox .m-favbtn').click();
                                }
                                $('#topNavLeft').html(r.header);
                                $('.ui-dialog-close').click();
                            }
                        });
                    }
                });

                $("#login-dialog").on("click",'#loginBtnBySms-dialog', function(){
                    var isValidAccount=ht.util.login.validate.chkAccount($('#account-dialog-sms'),$('#login-form-sms'));
                    if(!isValidAccount) {
                        return false
                    }
                    var isSmsKeyWord=ht.util.login.validate.chkSmskeyword($('#login-form-sms'));
                    if(!isSmsKeyWord) {
                        return false
                    }

                    if(isValidAccount && isSmsKeyWord ){
                        var param={
                            login_type:'phone',
                            phone: $('#account-dialog-sms').val(),
                            code  :$('#keyword-dialog-sms').val(),
                            _xsrf:$('input[name=_xsrf]').val()
                        }
                        $.post('/login.html',param,function(r){
                            var r=JSON.parse(r);
                            if(r.state!=200){
                                ht.util.login.labelErr.show(r.info,$('#login-form-sms'));
                                return false;
                            }else{
                                if($('#toTelRegister')[0]){
                                    window.location.href=ht.util.login.getNext();
                                    return false;
                                }
                                $('#topNavLeft').html(r.header);
                                $('.ui-dialog-close').click();
                            }
                        });
                    }
                });


            }
        },
        catalog:{
            init:function(){
                $('.mod-catalog li').hover(function(){
                    $(this).addClass('active');
                },function(){
                    $(this).removeClass('active');
                })
                $('.item-catalog .btn-close').click(function(){
                    $(this).parent().parent().removeClass('active');
                });
            }
        },
        slider:{
            init:function(){
                $(".prev,.next").hover(function(){
                    $(this).stop(true,false).fadeTo("show",0.9);
                },function(){
                    $(this).stop(true,false).fadeTo("show",0.4);
                });
                $(".banner-box").slide({
                    titCell:".hd ul",
                    mainCell:".bd ul",
                    effect:"fold",
                    interTime:3500,
                    delayTime:500,
                    autoPlay:true,
                    autoPage:true,
                    trigger:"click"
                });
            }
        }

    };
    $(function(){
        ht.util.init();
    });
})(window);;