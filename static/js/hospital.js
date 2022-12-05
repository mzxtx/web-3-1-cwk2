function sortTable(tablename,n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById(tablename);
    switching = true;
    // 设置升序排列
    dir = "asc";
    /* 设置一个循环语句 */
    while (switching) {
        // 设置循环结束标记
        switching = false;
        rows = table.rows;
        /* 循环列表，从第二行开始 */
        for (i = 1; i < (rows.length - 1); i++) {
            // 设置元素是否调换位置
            shouldSwitch = false;
            /* 获取要比较的元素,
            one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /* 判断是否将下一个元素与当前元素进行切换 (asc 或 desc):  */
            if (dir == "asc") {
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    // 设置调换元素标记，并结束当前循环
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    // 设置调换元素标记，并结束当前循环
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /* 如果元素调换位置设置为 true，则进行对调操作 */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // 每次对调完成时，将 switchcount 增加 1
            switchcount++;
        } else {
            /* 如果完成所有元素的排序且 direction 设置为 "asc",这时就将 direction 设置为 "desc" 并再次执行循环 */
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

function sortNum(tablename,n) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.getElementById("serve_adm_table");
    switching = true;
    // 设置升序排列
    dir = "asc";
    /* 设置一个循环语句 */
    while (switching) {
        // 设置循环结束标记
        switching = false;
        rows = table.rows;
        /* 循环列表，从第二行开始 */
        for (i = 1; i < (rows.length - 1); i++) {
            // 设置元素是否调换位置
            shouldSwitch = false;
            /* 获取要比较的元素,
            one from current row and one from the next: */
            x = rows[i].getElementsByTagName("TD")[n];
            y = rows[i + 1].getElementsByTagName("TD")[n];
            /* 判断是否将下一个元素与当前元素进行切换 (asc 或 desc):  */
            if (dir == "asc") {
                if (Number(x.innerHTML) > Number(y.innerHTML)) {
                    // 设置调换元素标记，并结束当前循环
                    shouldSwitch = true;
                    break;
                }
            } else if (dir == "desc") {
                if (Number(x.innerHTML) < Number(y.innerHTML)) {
                    // 设置调换元素标记，并结束当前循环
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            /* 如果元素调换位置设置为 true，则进行对调操作 */
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            // 每次对调完成时，将 switchcount 增加 1
            switchcount++;
        } else {
            /* 如果完成所有元素的排序且 direction 设置为 "asc",这时就将 direction 设置为 "desc" 并再次执行循环 */
            if (switchcount == 0 && dir == "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }
}

(function($){
    //插件
    $.extend($,{
        //命名空间
        sortTime:{
            sort:function(tableId,Idx){
                var table = document.getElementById(tableId);
                var tbody = table.tBodies[0];
                var tr = tbody.rows;

                var trValue = new Array();
                for (var i=0; i<tr.length; i++ ) {
                    trValue[i] = tr[i];  //将表格中各行的信息存储在新建的数组中
                }

                if (tbody.sortCol == Idx) {
                    trValue.reverse(); //如果该列已经进行排序过了，则直接对其反序排列
                } else {
                    //trValue.sort(compareTrs(Idx));  //进行排序
                    trValue.sort(function(tr1, tr2){
                        var value1 = tr1.cells[Idx].innerHTML;
                        var value2 = tr2.cells[Idx].innerHTML;
                        return value1.localeCompare(value2);
                    });
                }

                var fragment = document.createDocumentFragment();  //新建一个代码片段，用于保存排序后的结果
                for (var i=0; i<trValue.length; i++ ) {
                    fragment.appendChild(trValue[i]);
                }

                tbody.appendChild(fragment); //将排序的结果替换掉之前的值
                tbody.sortCol = Idx;
            }
        }
    });
})(jQuery);