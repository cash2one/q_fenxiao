(function( window, undefined ) {
    htRegister={
        init:function(){
            ht.util.placeholder();
            this.bindEvent();
        },
        validate:{
            chkPhone:function(){
                var isOk=false;
                var $phone=$('#phone');
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
                    $kapkey.parent().parent().next('.error').html('请输入验证码');
                    $kapkey.parent().removeClass('err_label').addClass('err_label');
                }else if($kapkey.val().length!=5){
                    $kapkey.parent().parent().next('.error').html('验证码错误');
                    $kapkey.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $kapkey.parent().parent().next('.error').html('');
                    $kapkey.parent().removeClass('err_label');
                    isOk=true;
                }
                return isOk;
            },
            chkSmsCode:function(){
                var isOk=false;
                var $smskey=$('#smskey');
                if($smskey.val()==''){
                    $smskey.parent().parent().next('.error').html('请输入短信验证码');
                    $smskey.parent().removeClass('err_label').addClass('err_label');
                }else if($smskey.val().length!=4){
                    $smskey.parent().parent().next('.error').html('短信验证码错误');
                    $smskey.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $smskey.parent().parent().next('.error').html('');
                    $smskey.parent().removeClass('err_label');
                    isOk=true;
                }
                return isOk;
            },
            chkPassword:function($obj){
                var isOk=false;
                if($obj.val().length<6 || $obj.val().length>18){
                    $obj.parent().next('.error').html('请输入6-18位字符');
                    $obj.parent().removeClass('err_label').addClass('err_label');
                }else{
                    $obj.parent().next('.error').html('');
                    $obj.parent().removeClass('err_label');
                    isOk=true;
                }
                return isOk;
            }

        },
        bindEvent:function(){
            $('#imgKey').click(function(){
                $(this)[0].src='/common/image_code/?'+Math.random();
            });
            var $acceptFlyme=$('#acceptFlyme');
            var $acceptError=$('#acceptError')
            $("#rememberField .mzchkbox").click(function(){
                if($acceptFlyme[0].checked){
                    $acceptFlyme[0].checked=false;
                    $('.checkboxPic').removeClass('check_chk').addClass('check_unchk');
                    $acceptError.show();

                }else{
                    $acceptFlyme[0].checked=true;
                    $('.checkboxPic').removeClass('check_unchk').addClass('check_chk');
                    $acceptError.hide();
                }
            });

            var $phone=$('#phone');
            var $kapkey=$('#kapkey');
            var $smskey=$('#smskey');
            $phone.focus(function(){}).blur(function(){
                htRegister.validate.chkPhone();
            });
            $kapkey.focus(function(){}).blur(function(){
                htRegister.validate.chkKapkey();
            }).keyup(function(e){
                if(e.keyCode==13){
                    $('#register').click();
                }
            });
            $smskey.blur(function(){
                htRegister.validate.chkSmsCode();
            }).keyup(function(e){
                if(e.keyCode==13){
                    $('#next').click();
                }
            });

            $('#register').click(function(){
                $('#spanerr').html('');
                var isPhone=htRegister.validate.chkPhone();
                var isKapKey=htRegister.validate.chkKapkey();
                if(isPhone&&isKapKey){
                    if(!$acceptFlyme[0].checked)
                    {
                        return false;
                    }
                    var _xsrf=$('input[name=_xsrf]').val();
                    var param={
                        phone: $phone.val(),
                        code:$kapkey.val(),
                        _xsrf:_xsrf
                    }

                    $.post('/reg.html',param,function(r){
                        var r=JSON.parse(r);
                        if(r.state!=200){
                            $('#spanerr').html(r.info);
                            return false;
                        }
                        $('#step2_txt').html(r.info);
                        $('.step1').hide();
                        $('.step2').show();
                        var timeline=60;
                        $('#getKey').html('重新获取('+timeline+')').attr('v',timeline).addClass("btn_enabled");
                        ht.util.setCountDown($('#getKey'),'获取验证码');
                    });


                }
            });

            $('#next').click(function(){
                var isSmsCode=htRegister.validate.chkSmsCode();
                if(isSmsCode){
                    var param={
                        phone: $phone.val(),
                        phonecode:$('#smskey').val()
                    }
                    $.get('/reg.html',param,function(r){
                        var r=JSON.parse(r);
                        if(r.state!=200){
                            $('#spansmskeyerr').html(r.info);
                            return false;
                        }
                        $('.step2').hide();
                        $('.step3').show();
                    });

                }
            });

            $('#getKey').click(function(){
                if($(this).hasClass('btn_enabled')) {
                    return false;
                }
                var param={
                    phone:$phone.val()
                }
                $.get('/common/phone/code/',param,function(){
                    var timeline=60;
                    $('#getKey').html('重新获取('+timeline+')').attr('v',timeline).addClass("btn_enabled");
                    ht.util.setCountDown($('#getKey'),'获取验证码');
                });

            });

            $('#password1').blur(function(){
                htRegister.validate.chkPassword($(this));
            });

            $('#password2').blur(function(){
                htRegister.validate.chkPassword($(this));
            }).keyup(function(e){
                if(e.keyCode==13){
                    $('#regSubmit').click();
                }
            });;

            $('#regSubmit').click(function(){
                var isPwd1=htRegister.validate.chkPassword($('#password1'));
                var isPwd2=htRegister.validate.chkPassword($('#password2'));
                if(isPwd1 && isPwd2){
                    if($('#password1').val()!=$('#password2').val()){
                        $('#password2').parent().next('.error').html('两次密码输入不一致');
                        $('#password2').parent().removeClass('err_label').addClass('err_label');
                    }
                    else{
                        var _xsrf=$('input[name=_xsrf]').val();
                        var param={
                            phone: $phone.val(),
                            pwd:$('#password1').val(),
                            smskey:$('#smskey').val(),
                            option:'reg',
                            _xsrf:_xsrf
                        }

                        $.post('/reg.html',param,function(r){
                            var r=JSON.parse(r);
                            if(r.state!=200){
                                $('#pwderr').html(r.info);
                                return false;
                            }else{
                                window.location='/';
                            }
                        });


                    }
                }

            });
        }
    }
    $(function(){
        htRegister.init();
    });
})(window);
