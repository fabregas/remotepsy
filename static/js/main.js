
function login() {
    $.post('/ru/login/', $('.form-signin').serialize()).
        done(function(data) {
            $(location).attr('href', '/');
        }).fail(function(data) {
            if (data.status == 401) {
                $('#authError').html('Неверный логин/пароль!')
            } else if (data.status == 403) {
                $('#authError').html('Пользователь заблокирован!')
            } else {
                $('#authError').html('Ошибка сервера!')
            }
        });
}

function logout() {
    $.post('/ru/logout/').done(function(data) {
            $(location).attr('href', '/');
        }).fail(function(data) {
            alert(data.statusText);
        });
}

function go_to_registration() {
    $(location).attr('href', '/registration');
}

function go_home() {
    $(location).attr('href', '/');
}

function go_to(path) {
    $(location).attr('href', path);
}

function show_message(header, message) {
   message = message.split('\n').join('<br/>')
   $('.base_container').html('<div class="jumbotron"><h2><b>' + header + '!</b></h2><h3>' + message + '</h3>' + 
          '<button class="btn btn-large btn-primary" onclick="location.href=\'/\'"});">OK</button></div>'); 
}

function ask_restore_password() {
    if ($('#inputEmail').val().length == 0) return;
    $('#restore_pwd_btn').prop('disabled', true);

    $.post($(location).attr('href'), $('.form-reg').serialize()).
        done(function(data) {
            console.log(data);
            $('#authError').html('');
            show_message(data['header'], data['message'])
        }).fail(function(data) {
            console.log(data);
            $('#restore_pwd_btn').prop('disabled', false);
            $('#authError').html('Error: ' + data.statusText);
        });
}
function set_password() {
    if ($('#inputPassword').val() != $('#inputPassword2').val()) {
        $('#authError').html('Пароли не совпадают!');
        return;
    }
    $.post($(location).attr('href'), $('.form-reg').serialize()).
        done(function(data) {
            console.log(data);
            $('#authError').html('');
            show_message(data['header'], data['message'])
        }).fail(function(data) {
            $('#authError').html('Ошибка: ' + data.statusText);
        });
}

function registration() {
    if ($('#inputPassword').val() != $('#inputPassword2').val()) {
        $('#authError').html('Пароли не совпадают!');
        return;
    }
    $.post('/ru/registration/', $('.form-reg').serialize()).
        done(function(data) {
            $('#authError').html('');
            show_message(data['header'], data['message'])
        }).fail(function(data) {
            $('#authError').html('Ошибка: ' + data.statusText);
        });

}

function set_lang(lang_code) {
    $.post('/i18n/setlang/', {language: lang_code}).
        done(function(data) {
            go_home();
        }).fail(function(data) {
            console.log(data);
            //go_home();
        });
}

$(function() {
    $('.form-signin').submit(function() {
          return false;
    });
    $('.form-reg').submit(function() {
          return false;
    });

});
