(function( window, undefined ) {
    htLogin={
        init:function(){
            ht.util.placeholder();
            this.bindEvent();
            this.switchTab();
        },
        switchTab:function(){
            $('#loginTab a').click(function(){
               $(this).addClass('active').siblings().removeClass('active');
                var index=$(this).index();
                $('.boxwrap').eq(index).show().siblings('.boxwrap').hide();
            });
        },
        validate:{
            chkPhone:function($obj){
                var isOk=false;
                var $phone=$obj;
                if($phone.val()==''){
                    $phone.parent().next('.error').html('请输入手机号码');
                    $phone.parent().removeClass('err_label').addClass('err_label');
                }else if (!/^1\d{10}$/.test($phone.val())){
                    $phone.parent().next('.error').html('手机号码格式不正确');
                    $phone.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $phone.parent().next('.error').html('');
                    $phone.parent().removeClass('err_label');
                    isOk=true;
                }
                return isOk;
            },
            chkKapkey:function(){
                var isOk=false;
                var $kapkey=$('#kapkey');
                if($kapkey.val()==''){
                    $kapkey.parent().next('.error').html('请输入图片验证码');
                    $kapkey.parent().removeClass('err_label').addClass('err_label');
                }else if($kapkey.val().length!=6){
                    $kapkey.parent().next('.error').html('图片验证码错误');
                    $kapkey.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $kapkey.parent().next('.error').html('');
                    $kapkey.parent().removeClass('err_label');
                    isOk=true;
                }
                isOk=true;
                return isOk;
            },
            chkSmsCode:function(){
                var isOk=false;
                var $smskey=$('#smskey');
                if($smskey.val()==''){
                    $smskey.parent().next('.error').html('请输入短信验证码');
                    $smskey.parent().removeClass('err_label').addClass('err_label');
                }else if($smskey.val().length!=6){
                    $smskey.parent().next('.error').html('短信验证码错误');
                    $smskey.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $smskey.parent().next('.error').html('');
                    $smskey.parent().removeClass('err_label');
                    isOk=true;
                }
                return isOk;
            },
            chkPassword:function($obj){
                var isOk=false;
                if($obj.val().length<6 || $obj.val().length>18){
                    $obj.parent().next('.error').html('请输入正确的密码');
                    $obj.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $obj.parent().next('.error').html('');
                    $obj.parent().removeClass('err_label');
                    isOk=true;
                }
                return isOk;
            },
            chkSmskeyword:function($obj){
                var isOk=false;
                if($obj.val().length!=4){
                    $obj.parent().parent().next('.error').html('请输入动态密码');
                    $obj.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $obj.parent().parent().next('.error').html('');
                    $obj.parent().removeClass('err_label');
                    isOk=true;
                }
                return isOk;
            }

        },
        bindEvent:function(){
            var $phone=$('#phone');
            var $kapkey=$('#kapkey');
            var $password=$('#password');
            $phone.focus(function(){}).blur(function(){
                htLogin.validate.chkPhone($phone);
            });
            $password.blur(function(){
                htLogin.validate.chkPassword($password);
            }).keyup(function(e){
                if(e.keyCode==13){
                    $('#phoneloginBtn').click();
                }
            });
            $kapkey.focus(function(){}).blur(function(){
                htLogin.validate.chkKapkey();
            });

            $('#phoneloginBtn').click(function(){
                var isPhone=htLogin.validate.chkPhone($phone);
                var isPwd=htLogin.validate.chkPassword($password);
                if(isPhone&&isPwd){

                    var param={
                        login_type:'usename',
                        usename: $phone.val(),
                        password :$password.val(),
                        _xsrf:$('input[name=_xsrf]').val()
                    }
                    $.post('/login.html',param,function(r){
                        var r=JSON.parse(r);
                        if(r.state!=200){
                            $('#LoginAccountInfo').html(r.info).show();
                            return false;
                        }else{
                            window.location.href= ht.util.login.getNext();
                        }
                    });
                }
            });

            $('#getKeyWord').click(function(){
                var $smsphone=$('#smsphone');
                var isSmsphone=htLogin.validate.chkPhone($smsphone);
                if(!isSmsphone){
                    return false;
                }
                if($(this).hasClass('btn_enabled')) {
                    return false;
                }
                var param={
                    phone:$smsphone.val()
                }
                var timeline=60;
                $('#getKeyWord').html('重新获取('+timeline+')').attr('v',timeline).addClass("btn_enabled");
                $.get('/common/phone/code/',param,function(){
                    ht.util.setCountDown($('#getKeyWord'),'获取动态密码');
                });
            });

            $('#smsloginBtn').click(function(){
                var $smsphone=$('#smsphone');
                var $smskeyword=$('#smskeyword');
                var isSmsphone=htLogin.validate.chkPhone($smsphone);
                var isSmskeyword=htLogin.validate.chkSmskeyword($smskeyword);
                if(isSmsphone&&isSmskeyword){
                    var param={
                        login_type:'phone',
                        phone: $smsphone.val(),
                        code  :$smskeyword.val(),
                        _xsrf:$('input[name=_xsrf]').val()
                    }
                    $.post('/login.html',param,function(r){
                        var r=JSON.parse(r);
                        if(r.state!=200){
                            $('#LoginPhoneInfo').html(r.info).show();
                            return false;
                        }else{
                            window.location.href= ht.util.login.getNext();
                        }
                    });
                }
            });
        }
    }
    $(function(){
        htLogin.init();
    });
})(window);
