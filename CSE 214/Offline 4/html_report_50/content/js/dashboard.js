/*
   Licensed to the Apache Software Foundation (ASF) under one or more
   contributor license agreements.  See the NOTICE file distributed with
   this work for additional information regarding copyright ownership.
   The ASF licenses this file to You under the Apache License, Version 2.0
   (the "License"); you may not use this file except in compliance with
   the License.  You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
var showControllersOnly = false;
var seriesFilter = "";
var filtersOnlySampleSeries = true;

/*
 * Add header in statistics table to group metrics by category
 * format
 *
 */
function summaryTableHeader(header) {
    var newRow = header.insertRow(-1);
    newRow.className = "tablesorter-no-sort";
    var cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Requests";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 3;
    cell.innerHTML = "Executions";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 7;
    cell.innerHTML = "Response Times (ms)";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 1;
    cell.innerHTML = "Throughput";
    newRow.appendChild(cell);

    cell = document.createElement('th');
    cell.setAttribute("data-sorter", false);
    cell.colSpan = 2;
    cell.innerHTML = "Network (KB/sec)";
    newRow.appendChild(cell);
}

/*
 * Populates the table identified by id parameter with the specified data and
 * format
 *
 */
function createTable(table, info, formatter, defaultSorts, seriesIndex, headerCreator) {
    var tableRef = table[0];

    // Create header and populate it with data.titles array
    var header = tableRef.createTHead();

    // Call callback is available
    if(headerCreator) {
        headerCreator(header);
    }

    var newRow = header.insertRow(-1);
    for (var index = 0; index < info.titles.length; index++) {
        var cell = document.createElement('th');
        cell.innerHTML = info.titles[index];
        newRow.appendChild(cell);
    }

    var tBody;

    // Create overall body if defined
    if(info.overall){
        tBody = document.createElement('tbody');
        tBody.className = "tablesorter-no-sort";
        tableRef.appendChild(tBody);
        var newRow = tBody.insertRow(-1);
        var data = info.overall.data;
        for(var index=0;index < data.length; index++){
            var cell = newRow.insertCell(-1);
            cell.innerHTML = formatter ? formatter(index, data[index]): data[index];
        }
    }

    // Create regular body
    tBody = document.createElement('tbody');
    tableRef.appendChild(tBody);

    var regexp;
    if(seriesFilter) {
        regexp = new RegExp(seriesFilter, 'i');
    }
    // Populate body with data.items array
    for(var index=0; index < info.items.length; index++){
        var item = info.items[index];
        if((!regexp || filtersOnlySampleSeries && !info.supportsControllersDiscrimination || regexp.test(item.data[seriesIndex]))
                &&
                (!showControllersOnly || !info.supportsControllersDiscrimination || item.isController)){
            if(item.data.length > 0) {
                var newRow = tBody.insertRow(-1);
                for(var col=0; col < item.data.length; col++){
                    var cell = newRow.insertCell(-1);
                    cell.innerHTML = formatter ? formatter(col, item.data[col]) : item.data[col];
                }
            }
        }
    }

    // Add support of columns sort
    table.tablesorter({sortList : defaultSorts});
}

$(document).ready(function() {

    // Customize table sorter default options
    $.extend( $.tablesorter.defaults, {
        theme: 'blue',
        cssInfoBlock: "tablesorter-no-sort",
        widthFixed: true,
        widgets: ['zebra']
    });

    var data = {"OkPercent": 92.75, "KoPercent": 7.25};
    var dataset = [
        {
            "label" : "FAIL",
            "data" : data.KoPercent,
            "color" : "#FF6347"
        },
        {
            "label" : "PASS",
            "data" : data.OkPercent,
            "color" : "#9ACD32"
        }];
    $.plot($("#flot-requests-summary"), dataset, {
        series : {
            pie : {
                show : true,
                radius : 1,
                label : {
                    show : true,
                    radius : 3 / 4,
                    formatter : function(label, series) {
                        return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'
                            + label
                            + '<br/>'
                            + Math.round10(series.percent, -2)
                            + '%</div>';
                    },
                    background : {
                        opacity : 0.5,
                        color : '#000'
                    }
                }
            }
        },
        legend : {
            show : true
        }
    });

    // Creates APDEX table
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.9275, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [1.0, 500, 1500, "/-28"], "isController": false}, {"data": [0.52, 500, 1500, "/notices-43"], "isController": false}, {"data": [0.96, 500, 1500, "/login-59"], "isController": false}, {"data": [1.0, 500, 1500, "/login-59-2"], "isController": false}, {"data": [0.94, 500, 1500, "/courses-48"], "isController": false}, {"data": [1.0, 500, 1500, "/api/download/256-71"], "isController": false}, {"data": [1.0, 500, 1500, "/login-59-0"], "isController": false}, {"data": [1.0, 500, 1500, "/login-59-1"], "isController": false}]}, function(index, item){
        switch(index){
            case 0:
                item = item.toFixed(3);
                break;
            case 1:
            case 2:
                item = formatDuration(item);
                break;
        }
        return item;
    }, [[0, 0]], 3);

    // Create statistics table
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 400, 29, 7.25, 89.87499999999997, 3, 456, 40.5, 265.80000000000007, 315.95, 387.0, 4.059677255658175, 159.32052737744849, 2.2250916599005377], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["/-28", 50, 0, 0.0, 31.84, 12, 88, 29.0, 47.8, 64.14999999999998, 88.0, 0.5100895717287957, 1.2124590015506722, 0.17335075289220786], "isController": false}, {"data": ["/notices-43", 50, 24, 48.0, 265.86, 120, 395, 275.0, 384.6, 387.9, 395.0, 0.5095593330887449, 3.7410811192980313, 0.1766538703579145], "isController": false}, {"data": ["/login-59", 50, 2, 4.0, 79.91999999999997, 41, 326, 72.5, 98.69999999999999, 191.84999999999926, 326.0, 0.5105739872764962, 1.1742204492540513, 0.7648637660958449], "isController": false}, {"data": ["/login-59-2", 50, 0, 0.0, 6.900000000000002, 4, 33, 5.0, 12.899999999999999, 16.799999999999983, 33.0, 0.5108400253376653, 0.7707498429166922, 0.24793700448517542], "isController": false}, {"data": ["/courses-48", 50, 3, 6.0, 238.51999999999998, 175, 456, 237.5, 269.9, 303.44999999999993, 456.0, 0.509741153442282, 22.105542383702556, 0.17671690378125987], "isController": false}, {"data": ["/api/download/256-71", 50, 0, 0.0, 23.299999999999997, 16, 64, 20.0, 35.9, 42.79999999999998, 64.0, 0.510662635836261, 130.868770394589, 0.18152460883242094], "isController": false}, {"data": ["/login-59-0", 50, 0, 0.0, 60.660000000000004, 29, 267, 59.0, 81.0, 90.35, 267.0, 0.5106209150326798, 0.25630776399101307, 0.2762538934844771], "isController": false}, {"data": ["/login-59-1", 50, 0, 0.0, 12.0, 3, 232, 6.0, 15.0, 17.0, 232.0, 0.5108348062403579, 0.14766318617885346, 0.2409504017715751], "isController": false}]}, function(index, item){
        switch(index){
            // Errors pct
            case 3:
                item = item.toFixed(2) + '%';
                break;
            // Mean
            case 4:
            // Mean
            case 7:
            // Median
            case 8:
            // Percentile 1
            case 9:
            // Percentile 2
            case 10:
            // Percentile 3
            case 11:
            // Throughput
            case 12:
            // Kbytes/s
            case 13:
            // Sent Kbytes/s
                item = item.toFixed(2);
                break;
        }
        return item;
    }, [[0, 0]], 0, summaryTableHeader);

    // Create error table
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["The operation lasted too long: It took 326 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 324 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 6.896551724137931, 0.5], "isController": false}, {"data": ["The operation lasted too long: It took 381 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 387 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 6.896551724137931, 0.5], "isController": false}, {"data": ["The operation lasted too long: It took 360 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 310 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 456 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 294 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 316 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 371 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 395 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 320 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 296 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 337 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 291 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 347 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 6.896551724137931, 0.5], "isController": false}, {"data": ["The operation lasted too long: It took 289 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 331 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 315 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 389 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 282 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 281 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 330 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 357 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 385 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 287 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, 3.4482758620689653, 0.25], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 400, 29, "The operation lasted too long: It took 324 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 387 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 347 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 326 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "The operation lasted too long: It took 381 milliseconds, but should not have lasted longer than 280 milliseconds.", 1], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": [], "isController": false}, {"data": ["/notices-43", 50, 24, "The operation lasted too long: It took 324 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 387 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 347 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 381 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "The operation lasted too long: It took 360 milliseconds, but should not have lasted longer than 280 milliseconds.", 1], "isController": false}, {"data": ["/login-59", 50, 2, "The operation lasted too long: It took 326 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "The operation lasted too long: It took 287 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "", "", "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["/courses-48", 50, 3, "The operation lasted too long: It took 315 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "The operation lasted too long: It took 456 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "The operation lasted too long: It took 294 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "", "", "", ""], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
