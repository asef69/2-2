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

    var data = {"OkPercent": 93.0, "KoPercent": 7.0};
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
    createTable($("#apdexTable"), {"supportsControllersDiscrimination": true, "overall": {"data": [0.93, 500, 1500, "Total"], "isController": false}, "titles": ["Apdex", "T (Toleration threshold)", "F (Frustration threshold)", "Label"], "items": [{"data": [0.99, 500, 1500, "/-28"], "isController": false}, {"data": [0.54, 500, 1500, "/notices-43"], "isController": false}, {"data": [0.96, 500, 1500, "/login-59"], "isController": false}, {"data": [1.0, 500, 1500, "/login-59-2"], "isController": false}, {"data": [0.95, 500, 1500, "/courses-48"], "isController": false}, {"data": [1.0, 500, 1500, "/api/download/256-71"], "isController": false}, {"data": [1.0, 500, 1500, "/login-59-0"], "isController": false}, {"data": [1.0, 500, 1500, "/login-59-1"], "isController": false}]}, function(index, item){
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
    createTable($("#statisticsTable"), {"supportsControllersDiscrimination": true, "overall": {"data": ["Total", 800, 56, 7.0, 89.90000000000002, 3, 419, 42.0, 257.9, 310.59999999999945, 393.96000000000004, 8.031080280686256, 315.1767653318342, 4.4018005932960556], "isController": false}, "titles": ["Label", "#Samples", "FAIL", "Error %", "Average", "Min", "Max", "Median", "90th pct", "95th pct", "99th pct", "Transactions/s", "Received", "Sent"], "items": [{"data": ["/-28", 100, 1, 1.0, 37.209999999999994, 11, 249, 34.5, 53.80000000000001, 72.49999999999989, 247.39999999999918, 1.0096522757562294, 2.3998961320221315, 0.34312401558903116], "isController": false}, {"data": ["/notices-43", 100, 46, 46.0, 266.1500000000001, 113, 419, 267.0, 385.9, 399.74999999999994, 418.92999999999995, 1.0070594870038974, 7.393626194624316, 0.34912706824842143], "isController": false}, {"data": ["/login-59", 100, 4, 4.0, 82.96999999999998, 37, 367, 71.5, 123.9, 193.5499999999999, 366.15999999999957, 1.0101724364348994, 2.3231993044962778, 1.5132856616124373], "isController": false}, {"data": ["/login-59-2", 100, 0, 0.0, 12.200000000000003, 3, 236, 6.0, 21.900000000000006, 44.799999999999955, 234.40999999999917, 1.0109996764801035, 1.5253852540642185, 0.4906902726666127], "isController": false}, {"data": ["/courses-48", 100, 5, 5.0, 222.69000000000005, 171, 346, 221.5, 267.8, 284.5999999999999, 345.70999999999987, 1.008532182261936, 43.736219353228314, 0.34963762178026103], "isController": false}, {"data": ["/api/download/256-71", 100, 0, 0.0, 27.55000000000001, 14, 167, 20.0, 40.60000000000002, 83.5499999999999, 166.75999999999988, 1.0108565998827406, 259.05470850686373, 0.359327931989568], "isController": false}, {"data": ["/login-59-0", 100, 0, 0.0, 59.74, 27, 272, 59.0, 81.9, 97.69999999999993, 270.5999999999993, 1.0103051121438675, 0.5071258082440897, 0.5465908516872096], "isController": false}, {"data": ["/login-59-1", 100, 0, 0.0, 10.689999999999996, 4, 77, 6.0, 17.0, 49.399999999999864, 76.97999999999999, 1.0109792344865236, 0.29223618496876075, 0.4768583693915927], "isController": false}]}, function(index, item){
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
    createTable($("#errorsTable"), {"supportsControllersDiscrimination": false, "titles": ["Type of error", "Number of errors", "% in errors", "% in all samples"], "items": [{"data": ["The operation lasted too long: It took 303 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 313 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 294 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 371 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 3.5714285714285716, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 293 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 283 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 400 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 344 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 355 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 323 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 302 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 3.5714285714285716, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 376 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 419 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 375 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 292 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 336 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 339 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 301 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 285 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 330 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 333 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 311 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 3.5714285714285716, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 346 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 3.5714285714285716, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 317 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 385 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 295 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 297 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 264 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 211 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 342 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 395 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 403 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 296 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 394 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 3.5714285714285716, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 291 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 347 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 373 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 331 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 249 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 354 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 386 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 367 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 409 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 328 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, 3.5714285714285716, 0.25], "isController": false}, {"data": ["The operation lasted too long: It took 380 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 412 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 361 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 322 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 338 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}, {"data": ["The operation lasted too long: It took 390 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, 1.7857142857142858, 0.125], "isController": false}]}, function(index, item){
        switch(index){
            case 2:
            case 3:
                item = item.toFixed(2) + '%';
                break;
        }
        return item;
    }, [[1, 1]]);

        // Create top5 errors by sampler
    createTable($("#top5ErrorsBySamplerTable"), {"supportsControllersDiscrimination": false, "overall": {"data": ["Total", 800, 56, "The operation lasted too long: It took 371 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 302 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 311 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 346 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 394 milliseconds, but should not have lasted longer than 280 milliseconds.", 2], "isController": false}, "titles": ["Sample", "#Samples", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors", "Error", "#Errors"], "items": [{"data": ["/-28", 100, 1, "The operation lasted too long: It took 249 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "", "", "", "", "", "", "", ""], "isController": false}, {"data": ["/notices-43", 100, 46, "The operation lasted too long: It took 371 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 394 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 311 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 328 milliseconds, but should not have lasted longer than 280 milliseconds.", 2, "The operation lasted too long: It took 297 milliseconds, but should not have lasted longer than 280 milliseconds.", 1], "isController": false}, {"data": ["/login-59", 100, 4, "The operation lasted too long: It took 283 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "The operation lasted too long: It took 264 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "The operation lasted too long: It took 211 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "The operation lasted too long: It took 367 milliseconds, but should not have lasted longer than 200 milliseconds.", 1, "", ""], "isController": false}, {"data": [], "isController": false}, {"data": ["/courses-48", 100, 5, "The operation lasted too long: It took 346 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "The operation lasted too long: It took 303 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "The operation lasted too long: It took 285 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "The operation lasted too long: It took 317 milliseconds, but should not have lasted longer than 280 milliseconds.", 1, "The operation lasted too long: It took 302 milliseconds, but should not have lasted longer than 280 milliseconds.", 1], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}, {"data": [], "isController": false}]}, function(index, item){
        return item;
    }, [[0, 0]], 0);

});
