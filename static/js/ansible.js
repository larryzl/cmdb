/**
 * Created by lei on 2018/11/5.
 */

var ansible = {};

ansible.itemList = [];

ansible.initButton = function(options){
    ansible.className = options.className || "";
    ansible.btnName = options.btnName || "";
    ansible.IDName = options.IDName ;
    ansible.updateList();

};

// 更新列表
ansible.updateList = function(){
    $("."+ansible.className).click(function(){
        $this = $(this);
        var itemData = JSON.stringify({
            uid: $this.val(),
            name: $this.html()
        });
        if($.inArray(itemData,ansible.itemList) == -1){
            ansible.itemList.push(itemData);
        }else {
            var index = ansible.itemList.indexOf(itemData);
            ansible.itemList.splice(index,1);
            //ansible.itemList.pop(itemData);
        }
        //console.log(ansible.itemList);
        ansible.addStyle();
        ansible.addButton();
    });

};
// 通过列表更新按钮样式
ansible.addStyle = function(){
    $("button[name="+ansible.btnName+"]").each(function(){
        $this = $(this);
        var itemData = JSON.stringify({
            uid: $this.val(),
            name: $this.html()
        });
        if($.inArray(itemData,ansible.itemList) == -1){
            $this.removeClass('btn-info').addClass('btn-default');
        }else {
            $this.removeClass('btn-default').addClass('btn-info');
        }
    });
};
// 更新选中按钮
ansible.addButton = function(){
    var btn_html = "";
    $("#"+ansible.IDName).html("");

    $.each(ansible.itemList,function(i,n){
        var json_n = JSON.parse(n);
        btn_html += '<button type="button" class="btn btn-info btn-xs btn-selected" name="btn-selected" value="'+json_n['uid']+'">' + json_n['name']+'</button>  ';
    });
    $("#select_num").html(ansible.itemList.length);
    $("#"+ansible.IDName).html(btn_html);
    ansible.removeBtn();
};

ansible.removeBtn = function(){
    $(".btn-selected").click(function(){

        var $this = $(this);
        var itemData = JSON.stringify({
            uid: $this.val(),
            name: $this.html()
        });
        console.log(itemData);

        var index = ansible.itemList.indexOf(itemData);
        ansible.itemList.splice(index,1);
        ansible.addStyle();
        ansible.addButton();
        console.log(ansible.itemList);
    })
};

ansible.checkAll = function(){
    $("button[name="+ansible.btnName+"]").each(function() {
        var $this = $(this);
        var itemData = JSON.stringify({
            uid: $this.val(),
            name: $this.html()
        });

        if($.inArray(itemData,ansible.itemList) == -1){
            ansible.itemList.push(itemData);
        }else {
            var index = ansible.itemList.indexOf(itemData);
            ansible.itemList.splice(index,1);
        }

        ansible.addStyle();
        ansible.addButton();
    })
};