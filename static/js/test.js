/**
 * Created by lei on 2018/10/23.
 */

var cmdb = {};

cmdb.initDataTable = function(options){
    var ele = options.ele || $('.dataTable');
  //   var columnDefs = [
  //    {
  //        targets: 0,
  //        orderable: false,
  //        createdCell: function (td, cellData) {
  //            $(td).html('<input type="checkbox" class="text-center ipt_check" id=99991937>'.replace('99991937', cellData));
  //        }
  //    },
  //    {className: 'text-center', targets: '_all'}
  //];
  //columnDefs = options.columnDefs ? options.columnDefs.concat(columnDefs) : columnDefs;
    var table = ele.DataTable({
        columns: options.columns || [],
        //order: options.order || [],
        language: {
            search: "搜索",
            lengthMenu: "每页  _MENU_",
            info: "显示第 _START_ 至 _END_ 项结果; 总共 _TOTAL_ 项",
            infoFiltered:   "",
            infoEmpty:      "",
            zeroRecords:    "没有匹配项",
            emptyTable:     "没有记录",
            paginate: {
                first:      "首页",
                previous:   "上一页",
                next:       "下一页",
                last:       "尾页"
            }
        }
    });
    return table;
};

cmdb.initServerDataTable = function (options) {
    var ele = options.ele || $(".dataTable");
    var columnDefs = [
        {
            targets: 0,
            orderable: false,
            createdCell: function (td, cellData) {
                $(td).html('<input type="checkbox" class="text-center ipt_check" data-uid=99991937>'.replace('99991937', cellData));
            }
        },
        {className: 'text-center', targets: '_all'}
    ];
    columnDefs = options.columnDefs ? options.columnDefs.concat(columnDefs) : columnDefs;
      var select = {
            style: 'multi',
            selector: 'td:first-child'
      };
    var table = ele.DataTable({
        language: {
            search: "搜索",
            lengthMenu: "每页  _MENU_",
            info: "显示第 _START_ 至 _END_ 项结果; 总共 _TOTAL_ 项",
            infoFiltered:   "",
            infoEmpty:      "",
            zeroRecords:    "没有匹配项",
            emptyTable:     "没有记录",
            paginate: {
                first:      "首页",
                previous:   "上一页",
                next:       "下一页",
                last:       "尾页"
            }
        },
        ajax: {
            url: options.ajax_url,
            dataType: 'json',
            type: 'POST',
//            data: {filter:JSON.stringify(options.columns)},
            headers:{'Content-Type': "application/x-www-form-urlencoded"},
            //data: function(data){
            //    console.log(data);
            //}
        },
        select: options.select || select,
        serverSide: true,
        processing: false,
        deferRender: true,
        pageLength: options.pageLength || 15,
        order: options.order || [],
        columnDefs: columnDefs,
        columns: options.columns || [],

        //"aoColumnDefs": [{
        //    "orderable": false,// 指定列不参与排序
        //    "aTargets": [0,7,9] // 指定 下标为[1,3,4,5,6]的不排序
        //}],
        lengthMenu: [[10, 15, 25, 50, -1], [10, 15, 25, 50, "All"]]
    });

    var table_id = table.settings()[0].sTableId;
    $('#' + table_id + ' .ipt_check_all').on('click', function() {
        if ($(this).prop("checked")) {
            $(this).closest('table').find('.ipt_check').prop('checked', true);
            //table.rows({search:'applied', page:'current'}).select();
        } else {
            $(this).closest('table').find('.ipt_check').prop('checked', false);
            //table.rows({search:'applied', page:'current'}).deselect();
        }
    });

    return table;
};