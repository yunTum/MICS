//改行なしのJSONデータ 動きます
  //var sample_json='[{"interested": 90,"age": 15,"gender": 0,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 100,"age": 25,"gender": 1,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 0,"age": null,"gender": null,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 10,"age": 45,"gender": 1,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 20,"age": 55,"gender": 0,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 30,"age": 65,"gender": 1,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 40,"age": 75,"gender": 0,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 50,"age": 15,"gender": 1,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 60,"age": 25,"gender": 0,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 70,"age": 35,"gender": 1,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 80,"age": 45,"gender": 0,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"},{"interested": 90,"age": 55,"gender": 1,"start_time": "2022-08-03 13:25:41","end_time": "2022-08-03 13:34:11"}]';


//改行有りのJSONデータ　動かないです　実際はこの形で帰ってくると思うのでこの状態で動くようにしたいです．
  var sample_json=
  [
     {
         "interested": 90,
         "age": 15,
         "gender": 0,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 100,
         "age": 25,
         "gender": 1,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 0,
         "age": null,
         "gender": null,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 10,
         "age": 45,
         "gender": 1
         ,"start_time": "2022-08-03 13:25:41"
         ,"end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 20,
         "age": 55,
         "gender": 0,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 30,
         "age": 65,
         "gender": 1,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 40,
         "age": 75,
         "gender": 0,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 50,
         "age": 15,
         "gender": 1,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 60,
         "age": 25,
         "gender": 0,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 70,
         "age": 35,
         "gender": 1,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 80,
         "age": 45,
         "gender": 0,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     },
     {
         "interested": 90,
         "age": 55,
         "gender": 1,
         "start_time": "2022-08-03 13:25:41",
         "end_time": "2022-08-03 13:34:11"
     }
 ];


 //JSONをparseして連想配列に変換
    var sample_arr = JSON.parse(sample_json);
    console.log(sample_arr);
    
    
//もとの連想配列を使いたいデータに編集
    //関心度別
    var nomal=70 ;
    
    var max_int_arr = sample_arr.filter(x => x.interested <=100 && x.interested>=nomal );
    console.log("関心度特に有り",max_int_arr);
    
    var nomal_int_arr = sample_arr.filter(x => x.interested <nomal && x.interested>0 );
    console.log("関心度有り",nomal_int_arr.length);
    
    var not_int_arr = sample_arr.filter(x => x.interested ===0 );
    console.log("関心度無し",not_int_arr.length);
    
    var all_int_arr=sample_arr.filter(x => x.interested <=100 && x.interested>0 );
    console.log("関心度特にあり＆有り",all_int_arr);
    
    //グラフデータ配列名
    A1_data=[max_int_arr.length,nomal_int_arr.length,not_int_arr.length];
    console.log(A1_data);
    
    
    
    //関心度男女別
    //特に有り
    var max_int_male = max_int_arr.filter(x => x.gender === 1);
    console.log("特に有り男",max_int_male);
    
    var max_int_female = max_int_arr.filter(x => x.gender === 0);
    console.log("特に有り女",max_int_female);
    
    //有り
    var all_int_mail = all_int_arr.filter(x => x.gender === 1);
    console.log("有り男",all_int_mail);
    
    var all_int_femail = all_int_arr.filter(x => x.gender === 0);
    console.log("有り女",all_int_femail);
    
    //グラフデータ配列名
    A21_data=[max_int_male.length,max_int_female.length];
    A22_data=[all_int_mail.length,all_int_femail.length];