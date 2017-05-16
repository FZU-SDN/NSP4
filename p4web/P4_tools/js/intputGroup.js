/** 
 * Created by DreamBoy on 2016/6/4. 
 */  
/** 
 * Created by DreamBoy on 2016/4/29. 
 */  
$(function() {  
    $.fn.initInputGroup = function (options) {  
        //1.Settings 初始化设置  
        var c = $.extend({  
            widget: 'input',  
            add: "<span class=\"glyphicon glyphicon-plus\"></span>",  
            del: "<span class=\"glyphicon glyphicon-minus\"></span>",  
            field: '',  
            data: []  
        }, options);  
  
        var _this = $(this);  
  
        //添加序号为1的输入框组  
        addInputGroup(1);  
  
        /** 
         * 添加序号为order的输入框组 
         * @param order 输入框组的序号 
         * @param data 初始化输入框组中的数据 
         */  
        function addInputGroup(order) {  
  
            //1.创建输入框组  
            var inputGroup = $("<div class='input-group' style='margin: 10px 0'></div>");  
            //2.输入框组的序号  
            var inputGroupAddon1 = $("<span class='input-group-addon'></span>");  
            //3.设置输入框组的序号  
            inputGroupAddon1.html(" " + order + " ");  
  
            //4.创建输入框组中的输入控件（input或textarea）  
            var widget = '', inputGroupAddon2;  
            if(c.widget == 'textarea') {  
                widget = $("<textarea class='form-control' style='resize: vertical;'></textarea>");  
                widget.html(c.data[order - 1]);  
                inputGroupAddon2 = $("<span class='input-group-addon'></span>");  
            } else if(c.widget == 'input') {  
                widget = $("<input class='form-control' type='text'/>");  
                widget.val(c.data[order - 1]);  
                inputGroupAddon2 = $("<span class='input-group-btn'></span>");  
            }  
  
            //5.设置表单提交时的字段名  
            if(c.field.length == 0) {  
                widget.prop('name', c.widget + 'Data[]');  
            } else {  
                widget.prop('name', c.field + '[]');  
            }  
  
  
            //6.创建输入框组中最后面的操作按钮  
            var addBtn = $("<button class='btn btn-default' type='button'>" + c.add + "</button>");  
            addBtn.appendTo(inputGroupAddon2).on('click', function() {  
                //7.响应删除和添加操作按钮事件  
                if($(this).html() == c.del) {  
                    $(this).parents('.input-group').remove();  
                } else if($(this).html() == c.add) {  
                    $(this).html(c.del);  
                    addInputGroup(order+1);  
                }  
                //8.重新排序输入框组的序号  
                resort();  
            });  
  
            inputGroup.append(inputGroupAddon1).append(widget).append(inputGroupAddon2);  
  
            _this.append(inputGroup);  
  
            if(order + 1 > c.data.length) {  
                return;  
            }  
            addBtn.trigger('click');  
        }  
  
        function resort() {  
            var child = _this.children();  
            $.each(child, function(i) {  
                $(this).find(".input-group-addon").eq(0).html(' ' + (i + 1) + ' ');  
            });  
        }  
    }  
});  