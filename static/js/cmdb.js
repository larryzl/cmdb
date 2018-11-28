/**
 * Created by lei on 2018/10/19.
 */

var checked=false;
function check_all(form) {
    var checkboxes = document.getElementById(form);
    if (checked === false) {
        checked = true;
    } else {
        checked = false;
    }
    for (var i = 0; i < checkboxes.elements.length; i++) {
        if (checkboxes.elements[i].type == "checkbox") {
            checkboxes.elements[i].checked = checked;
        }
    }
}

function APIUpdateAttr(props) {
    // props = {url: .., body: , success: , error: , method: ,}
    props = props || {};
    var success_message = props.success_message || '更新成功!';
    var fail_message = props.fail_message || '更新时发生未知错误.';
    var flash_message = props.flash_message || true;
    if (props.flash_message === false){
        flash_message = false;
    }
    //console.log(props.body);
    $.ajax({
        url: props.url,
        type: props.method || "PATCH",
        data: props.body,
        contentType: props.content_type || "application/json; charset=utf-8",
        dataType: props.data_type || "json"
    }).done(function(data, textStatue, jqXHR) {
        if (flash_message) {
            console.log('step 1');
            console.log(data);
            toastr.success(success_message);
        }
        if (typeof props.success === 'function') {
            console.log('step 2');
            console.log(data);
            return props.success(data);
        }

        if (props.data_table){
            console.log('step 3');

            props.data_table.ajax.reload();
        }
    }).fail(function(jqXHR, textStatus, errorThrown) {
        if (flash_message) {
            toastr.error(fail_message);
        }
        if (typeof props.error === 'function') {
            return props.error(jqXHR.responseText);
        }
    });
  // return true;
}



function objectActiveChange(obj,name,url,data_table,redirectTo){
    function doChange(){
        var body = {};
        var fail = function(){
            swal("错误","更新"+"[ "+name+" ]"+"遇到错误","error");
        };
        var success = function(){
            if (!redirectTo) {
                if(Array.isArray(obj)){
                    $.each(obj,function(i,j){
                        $(j).parent().parent().remove();
                    })
                }else {
                    $(obj).parent().parent().remove();
                }
            } else {
                setTimeout('window.location.reload()',2000);

            }
        };
        APIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: "GET",
            success_message: "更新成功",
            success: success,
            error: fail,
            data_table: data_table
        });
    }
    if(name.length == 0){
        swal({
            title: '没有选择项目!',
            text: "选项不能为空!",
            type: "error",
            confirmButtonText: '确认',
            closeOnConfirm: true
        },function(){
            return false;
        });
    }else {
        swal({
            title: '你确定修改状态吗 ?',
            text: " [" + name + "] ",
            type: "warning",
            showCancelButton: true,
            cancelButtonText: '取消',
            confirmButtonColor: "#ed5565",
            confirmButtonText: '确认',
            closeOnConfirm: true
        }, function () {
            doChange();
        });
    }

}

// Sweet Alert for Delete
function objectDelete(obj, name, url, redirectTo) {
    function doDelete() {
        var body = {};
        var success = function() {
            // swal('Deleted!', "[ "+name+"]"+" has been deleted ", "success");
            if (!redirectTo) {
                if(Array.isArray(obj)){
                    $.each(obj,function(i,j){
                        $(j).parent().parent().remove();
                    })
                }else {
                    $(obj).parent().parent().remove();
                }
            } else {
                window.location.href=redirectTo;
            }
        };
        var fail = function() {
            swal("错误", "删除"+"[ "+name+" ]"+"遇到错误", "error");
        };
        APIUpdateAttr({
            url: url,
            body: JSON.stringify(body),
            method: 'DELETE',
            success_message: "删除成功",
            success: success,
            error: fail
        });
    };
    //console.log(name.length);
    if(name.length == 0){
        swal({
            title: '没有选择项目!',
            text: "选项不能为空!",
            type: "error",
            confirmButtonText: '确认',
            closeOnConfirm: true
        },function(){
            return false;
        });
    }else {
        swal({
            title: '你确定删除吗 ?',
            text: " [" + name + "] ",
            type: "warning",
            showCancelButton: true,
            cancelButtonText: '取消',
            confirmButtonColor: "#ed5565",
            confirmButtonText: '确认',
            closeOnConfirm: true
        }, function () {
            doDelete()
        });
    };
}

/** 侧栏菜单 **/
function activeNav() {
    var url_array = document.location.pathname.split("/");
    var app = url_array[1];
    var resource = url_array[2];
    if (app === ''){
        $('#index').addClass('active');
    } else {
        $("#" + app).addClass('active');
        $('#' + app + ' #' + resource).addClass('active');
    }
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                // break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function setAjaxCSRFToken() {
    var csrftoken = getCookie('csrftoken');
    var sessionid = getCookie('sessionid');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
}
