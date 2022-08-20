/*
MICS Front
Grahp表示関係
*/

//指定した要素を子含めて全削除
function removeAll(element){
    while(element.firstChild){
        element.removeChild(element.firstChild);
    }
    element.remove();
}

//グラフ表示クラス
class MICSGrahp{
    //public--------------------------------------------------------------------------------------------

    //コンストラクタ
    constructor(MICS_class) {
        this.#AddGraphDOM();
        this.data = new DataIN(MICS_class.date_first, MICS_class.date_last, MICS_class.interest_data);
        this.#LoadGrahps();
    }

    //グラフの再描画
    Update(MICS_class){
        removeAll(document.getElementById("graphA" ))
        removeAll(document.getElementById("graphB" ))
        removeAll(document.getElementById("graphC" ))
        removeAll(document.getElementById("graphD1"))
        removeAll(document.getElementById("graphD2"))
        this.#AddGraphDOM();
        this.data = new DataIN(MICS_class.date_first, MICS_class.date_last, MICS_class.interest_data);
        this.#LoadGrahps();
    }

    //private-------------------------------------------------------------------------------------------
    
    //グラフの描画
    #LoadGrahps(){
        this.#GrahpA1();
        this.#GrahpA21();
        this.#GrahpA22();
        this.#GrahpB1();
        this.#GrahpB2();
        this.#GrahpC1();
        this.#GrahpD11();
        this.#GrahpD12();
        this.#GrahpD13();
        this.#GrahpD21();
        this.#GrahpD22();
        this.#GrahpD23();
    }

    //それぞれのグラフを表示する関数

    #GrahpA1(){
        const element = document.getElementById('graph_A1').getContext('2d');
        const chart = new Chart(element, {
            type:'pie',
            // データを指定
            data: {
                labels: ["特に関心有り", "関心有り", "関心なし"],
                datasets: [{
                    backgroundColor: [
                    'rgba(220, 53, 69, 1)'  ,
                    'rgba(255, 141, 152, 1)',
                    'rgba(138, 138, 138, 1)',
                    ],
                    data: this.data.A1_data
                }]
            },
       });
    }

    #GrahpA21(){
        const element = document.getElementById('graph_A21').getContext('2d');
        const chart = new Chart(element, {
            type:'pie',
            data: {
                labels: ["女性", "男性"],
                datasets: [{
                  backgroundColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)'
                  ],
                  data: this.data.A21_data
                }]
            },
       });
    }

    #GrahpA22(){
        const element = document.getElementById('graph_A22').getContext('2d');
        const chart = new Chart(element, {
            type:'pie',
            data: {
                labels: ["女性", "男性"],
                datasets: [{
                  backgroundColor: [
                  'rgba(255, 99, 132, 1)',
                  'rgba(54, 162, 235, 1)'
                  ],
                  data: this.data.A22_data
                }]
            },
       });
    }

    #GrahpB1(){
        const element = document.getElementById('graph_B1').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: ["男性", "女性"],
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.B1_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.B1_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.B1_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                    barPercentage:0.6,
                    label:           "40代",
                    data:            this.data.B1_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.B1_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.B1_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                },
                ],
                options: {
                    responsive: true,
                    indexAxis: "y",
                    plugins: {
                        stacked100: { enable: true },
                    },
                }
            },
       });
    }

    #GrahpB2(){
        const element = document.getElementById('graph_B2').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: ["男性", "女性"],
                datasets: [
                  {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.B2_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.B2_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.B2_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                    barPercentage:0.6,
                    label:           "40代",
                    data:            this.data.B2_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.B2_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                  barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.B2_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                },
                ],
                options: {
                    responsive: true,
                    indexAxis: "y",
                    plugins: {
                        stacked100: { enable: true },
                    }
                }
            },
       });
    }

    #GrahpC1(){
        const element = document.getElementById('graph_C1').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: this.data.label_time_arr,
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "関心度なし",
                    data:            this.data.C1_notint_data,
                    backgroundColor: "rgba(171, 171, 171, 0.8)",
                    borderColor:     "rgba(171, 171, 171, 1.0)",
                    borderWidth:     1,
                }, 
                {  
                    barPercentage:0.6,
                    label:           "関心度有り",
                    data:            this.data.C1_nomalint_data,
                    backgroundColor: "rgba(232, 123, 134, 0.8)",
                    borderColor:     "rgba(232, 123, 134, 1.0)",
                    borderWidth:     1,
                }, 
                {   
                    barPercentage:0.6,
                    label:           "関心度特に有り",
                    data:            this.data.C1_maxint_data,
                    backgroundColor: "rgba(220, 53, 69, 0.8)",
                    borderColor:     "rgba(220, 53, 69, 1.0)",
                    borderWidth:     1,
                }],
                
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            display:      true,
                            stacked:      true,
                            suggestedMax: 100,
                            suggestedMin: 0,
                            ticks: {
                            stepSize: 10,
                            },
                        },
                        y: {
                            display:      true,
                            stacked:      true,
                        }
                    }
                },
            }
        });
    }

    #GrahpD11(){
        const element = document.getElementById('graph_D11').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: this.data.label_time_arr,
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.D11_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.D11_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.D11_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                    barPercentage:0.6,
                    label:           "40代",
                    data:            this.data.D11_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.D11_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    borderRadius:5,
                    barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.D11_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                }
                ],
                option: {
                   responsive: true,
                   scales: {
                        x: {
                            display:      true,
                            stacked:      true,
                            suggestedMax: 100,
                            suggestedMin: 0,
                            ticks: {
                                stepSize: 10,
                            },
                        },
                        y: {
                            display:      true,
                            stacked:      true,
                        }
                    }
                }
            }
       });
    }

    #GrahpD12(){
        const element = document.getElementById('graph_D12').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: this.data.label_time_arr,
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.D12_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.D12_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.D12_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                barPercentage:0.6,
                label:               "40代",
                    data:            this.data.D12_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.D12_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    borderRadius:5,
                    barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.D12_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                }
                ],
                },
                option: {
                    responsive: true,
                    scales: {
                    x: {
                        display:      true,
                        stacked:      true,
                        suggestedMax: 100,
                        suggestedMin: 0,
                        ticks: {
                        stepSize: 10,
                        },
                    },
                    y: {
                        display:      true,
                        stacked:      true,
                    }
                }
            }
       });
    }

    #GrahpD13(){
        const element = document.getElementById('graph_D13').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: this.data.label_time_arr,
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.D13_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.D13_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.D13_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                    barPercentage:0.6,
                    label:           "40代",
                    data:            this.data.D13_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.D13_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    borderRadius:5,
                    barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.D13_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                }
                ],
                },
                option: {
                    responsive: true,
                    scales: {
                    x: {
                        display:      true,
                        stacked:      true,
                        suggestedMax: 100,
                        suggestedMin: 0,
                        ticks: {
                        stepSize: 10,
                        },
                    },
                    y: {
                        display:      true,
                        stacked:      true,
                    }
                }
            }
       });
    }

    #GrahpD21(){
        const element = document.getElementById('graph_D21').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: this.data.label_time_arr,
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.D21_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.D21_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.D21_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                    barPercentage:0.6,
                    label:           "40代",
                    data:            this.data.D21_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.D21_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    borderRadius:5,
                    barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.D21_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                }
                ],
                },
                option: {
                  responsive: true,
                   scales: {
                    x: {
                        display:      true,
                        stacked:      true,
                        suggestedMax: 100,
                        suggestedMin: 0,
                        ticks: {
                            stepSize: 10,
                        },
                    },
                    y: {
                        display:      true,
                        stacked:      true,
                    }
                }
            }
       });
    }

    #GrahpD22(){
        const element = document.getElementById('graph_D22').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {
                labels: this.data.label_time_arr,
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.D23_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    borderRadius:5,
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.D23_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.D23_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                    barPercentage:0.6,
                    label:           "40代",
                    data:            this.data.D23_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.D23_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    borderRadius:5,
                    barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.D23_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                }
                ],
                },
                option: {
                    responsive: true,
                    scales: {
                    x: {
                        display:      true,
                        stacked:      true,
                        suggestedMax: 100,
                        suggestedMin: 0,
                        ticks: {
                        stepSize: 10,
                        },
                    },
                    y: {
                        display:      true,
                        stacked:      true,
                    }
                }
            }
        });
    }

    #GrahpD23(){
        const element = document.getElementById('graph_D23').getContext('2d');
        const chart = new Chart(element, {
            type:'bar',
            data: {labels: this.data.label_time_arr,
                datasets: [
                {
                    barPercentage:0.6,
                    label:           "10代以下",
                    data:            this.data.D22_10_data,
                    backgroundColor: "rgba(220,53,69, 0.8)",
                    borderColor:     "rgba(220,53,69, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "20代",
                    data:            this.data.D22_20_data,
                    backgroundColor: "rgba(255,142,10, 0.8)",
                    borderColor:     "rgba(255,142,10, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "30代",
                    data:            this.data.D22_30_data,
                    backgroundColor: "rgba(255,228,88, 0.8)",
                    borderColor:     "rgba(255,228,88, 1.0)",
                    borderWidth:     1,
                },
                {
                    barPercentage:0.6,
                    label:           "40代",
                    data:            this.data.D22_40_data,
                    backgroundColor: "rgba(84,241,100, 0.8)",
                    borderColor:     "rgba(84,241,100, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    barPercentage:0.6,
                    label:           "50代",
                    data:            this.data.D22_50_data,
                    backgroundColor: "rgba(53,90,220, 0.8)",
                    borderColor:     "rgba(53,90,220, 1.0)",
                    borderWidth:     1,
                }, 
                {
                    borderRadius:5,
                    barPercentage:0.6,
                    label:           "60代以上",
                    data:            this.data.D22_60_data,
                    backgroundColor: "rgba(151,71,255, 0.8)",
                    borderColor:     "rgba(151,71,255, 1.0)",
                    borderWidth:     1,
                }
                ],
                },
                chartOptions: {
                    responsive: true,
                    scales: {
                    x: {
                        display:      true,
                        stacked:      true,
                        suggestedMax: 100,
                        suggestedMin: 0,
                        ticks: {
                            stepSize: 10,
                        },
                    },
                        y: {
                        display:      true,
                        stacked:      true,
                    }
                }
            }
        });
    }

    //HTMLにグラフ部分を追加するする関数
    #AddGraphDOM(){
        this.new_HTML_data = `
        <div class="graphA" id="graphA">
            <div class="graphA1">
                <div class="graphA1title">
                    <h1>関心度別人数比</h1>
                </div>
                <hr noshade>    
                <div class="graphA1inner">
                    <canvas id="graph_A1"></canvas>
                </div> 
            </div>
            <div class="graphA2">
                <div class="graphA2title">
                    <h1>関心度別男女比</h1>
                </div>
                <hr noshade> 
                <div class="graphA2inner">
                    <div class="A21">
                        <h2>特に関心あり</h2>
                        <canvas id="graph_A21" height=100%></canvas>
                    </div>
                    <div class="A22">
                        <h2>特に関心あり&関心あり</h2>
                        <canvas id="graph_A22"></canvas>
                    </div>
                </div>
            </div>                     
        </div>


        <div class="graphB" id="graphB">
            <div class="graphBtitle">
                <h1>関心度別男女年齢比</h1>
                
            </div>
            <hr noshade> 
            <div class="B1">
                <div class="B1h2"><h2>特に関心あり</h2></div>
                <div class="B1inner">
                    <canvas id="graph_B1" width="100" height="12"></canvas>
                </div>
            </div>
            <hr noshade> 
            <div class="B2">
                <div class="B2h2">
                <h2>特に関心あり</h2>
                <h2>&</h2>
                <h2>関心あり</h2>
                </div>
                <div class="B2inner">
                    <canvas id="graph_B2" width="100" height="12"></canvas>
                </div>
            </div>
        </div>

        <div class="graphC" id="graphC">
            <div class="graphCtitle">
                <h1>関心度時間推移</h1>
                
            </div>
            <div><hr noshade></div>
            
            <div class="C1">
                <canvas id="graph_C1" width="100" height="25"></canvas>
            </div>
        </div>

        <div class="graphD1" id="graphD1">
            <div class="graphD1title">
                <h1>【関心あり】年齢比時間推移</h1>
                
            </div>
            <hr noshade> 
            <div class="graphD11">
                <h2>全体</h2>
                <div class="graphD11inner">
                    <canvas id="graph_D11" width="100" height="20"></canvas>
                </div>
            </div>
            <hr>
            <div class="graphD12">
                <h2>男性</h2>
                <div class="graphD12inner">
                    <canvas id="graph_D12" width="100" height="20"></canvas>
                </div>
            </div>
            <hr>
            <div class="graphD13">
                <h2>女性</h2>
                <div class="graphD13inner">
                    <canvas id="graph_D13" width="100" height="20"></canvas>
                </div>
            </div>
        </div>

        <div class="graphD2" id="graphD2">
            <div class="graphD2title">
                <h1>【特に関心あり】年齢比時間推移</h1>
            </div>
            <hr noshade> 
            <div class="graphD21">
                <h2>全体</h2>
                <div class="graphD21inner">
                    <canvas id="graph_D21" width="100" height="20"></canvas>
                </div>
            </div>
            <hr>
            <div class="graphD22">
                <h2>男性</h2>
                <div class="graphD22inner">
                    <canvas id="graph_D22" width="100" height="20"></canvas>
                </div>
            </div>
            <hr>
            <div class="graphD23">
                <h2>女性</h2>
                <div class="graphD23inner">
                    <canvas id="graph_D23" width="100" height="20"></canvas>
                </div>         
            </div>
        </div>`;
    
        this.app_element = document.getElementById("app");
        this.app_element.insertAdjacentHTML('afterend', this.new_HTML_data);
    }
}