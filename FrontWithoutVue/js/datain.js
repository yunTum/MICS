/*
MICS Front
データ成形
*/
class DataIN{
    constructor(d1, d2, InterestData){
        
        //連想配列に変換
        var backdata_arr = JSON.parse(InterestData);
        
        //ユーザーの指定した時間計算
        var user_intime =d1;
        var user_outtime=d2;
        var bet_time=user_outtime-user_intime;

        //１日～31日までの場合1daymax31本
        var label_unix_in=[];
        if(bet_time<=2678400 && bet_time>=86400){
            
            //時間変化ラベル作成
            
            
            for(let h=0 ;h<user_outtime ;h=h+86400){
                label_unix_in.push(user_intime+h)
            }
            
            var label_time_arr=[]//ラベル名
            
            
            
            for(let i=0 ;i<31 ;i=i+1){
                var label_time_in= new Date(label_unix_in[i]*1000);
                
                var label_time_in_2=label_time_in.getMonth()+1+"/"+label_time_in.getDate()+"/ "+label_time_in.getHours()+":"+label_time_in.getMinutes()
                
                    label_time_arr.push(label_time_in_2);
                }
            
            
            
            //時間で分ける
            
            var backdata_arr_time=[];
            
            for(let i=0 ;i<2678400 ;i=i+86400){
                var backdata_arr_time_in= backdata_arr.filter(x => x.end_time_unix <= user_intime+(i+86400) && x.end_time_unix > user_intime+i );
                backdata_arr_time.push(backdata_arr_time_in);
            }
            
            //関心度で分ける
            var int_line=70
            
            
            var all_max_int_arr  = backdata_arr.filter(x => x.interested <=100 && x.interested>=int_line );
        
        
            var all_nomal_int_arr= backdata_arr.filter(x => x.interested <int_line && x.interested>0 );
        
        
            var all_all_int_arr  = backdata_arr.filter(x => x.interested <=100 && x.interested>0 );
        
        
            var all_not_int_arr  = backdata_arr.filter(x => x.interested ===0 );
            
            
            
            
            
            var max_int_arr=[];
            var nomal_int_arr=[];
            var all_int_arr=[];
            var not_int_arr=[];
            
            
            for(let i=0 ;i<31 ;i=i+1){
                var max_int_arr_in= backdata_arr_time[i].filter(x => x.interested <=100 && x.interested>=int_line );
                max_int_arr.push(max_int_arr_in);
            }
            for(let i=0 ;i<31 ;i=i+1){
                var nomal_int_arr_in= backdata_arr_time[i].filter(x => x.interested <int_line && x.interested>0 );
                nomal_int_arr.push(nomal_int_arr_in);
            }
            for(let i=0 ;i<31 ;i=i+1){
                var all_int_arr_in= backdata_arr_time[i].filter(x => x.interested <=100 && x.interested>0 );
                all_int_arr.push(all_int_arr_in);
            }
            for(let i=0 ;i<31 ;i=i+1){
                var not_int_arr_in= backdata_arr_time[i].filter(x => x.interested ===0 );
                not_int_arr.push(not_int_arr_in);
            }
            
            //性別で分ける
            
            var all_mail_max_int_arr_in= all_max_int_arr.filter(x => x.gender === 1);
            var all_femail_max_int_arr_in= all_max_int_arr.filter(x => x.gender === 0);
            var all_mail_all_int_arr_in= all_all_int_arr.filter(x => x.gender === 1);
            var all_femail_all_int_arr_in= all_all_int_arr.filter(x => x.gender === 0);
            
            
            
            var mail_max_int_arr=[];
            var femail_max_int_arr=[];
            
            var femail_all_int_arr=[];
            var mail_all_int_arr=[];
            
            for(let i=0 ;i<31 ;i=i+1){
                var mail_max_int_arr_in= max_int_arr[i].filter(x => x.gender === 1);
                mail_max_int_arr.push(mail_max_int_arr_in);
                
                var femail_max_int_arr_in= max_int_arr[i].filter(x => x.gender === 0);
                femail_max_int_arr.push(femail_max_int_arr_in);
            }
            
            for(let i=0 ;i<31 ;i=i+1){
                var mail_all_int_arr_in= all_int_arr[i].filter(x => x.gender === 1);
                mail_all_int_arr.push(mail_all_int_arr_in);
                
                var femail_all_int_arr_in= all_int_arr[i].filter(x => x.gender === 0);
                femail_all_int_arr.push(femail_all_int_arr_in);
            }
        
        
        
        
            //A1
            var A1_data=[all_max_int_arr  .length, all_nomal_int_arr.length , all_not_int_arr  .length]
            
            //A21
            var A21_data=[all_mail_max_int_arr_in.length ,all_femail_max_int_arr_in.length]
            
            //A22
            var A22_data=[all_mail_all_int_arr_in.length ,all_femail_all_int_arr_in.length]
            
            
            //C1
            var C1_maxint_data  =[];
            var C1_nomalint_data=[];
            var C1_notint_data  =[];
            
            for(let i=0;i<31;i++){
                C1_maxint_data.push(max_int_arr[i].length);
                C1_nomalint_data.push(nomal_int_arr[i].length);
                C1_notint_data.push(not_int_arr[i].length);
            }
        
        
            //B1
            var B1_mail_10_data=[];
            var B1_mail_20_data=[];
            var B1_mail_30_data=[];
            var B1_mail_40_data=[];
            var B1_mail_50_data=[];
            var B1_mail_60_data=[];
            var B1_femail_10_data=[];
            var B1_femail_20_data=[];
            var B1_femail_30_data=[];
            var B1_femail_40_data=[];
            var B1_femail_50_data=[];
            var B1_femail_60_data=[];

            var B1_mail_10_data_in= all_mail_max_int_arr_in.filter(x => x.age < 20);    
            var B1_mail_20_data_in= all_mail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);    
            var B1_mail_30_data_in= all_mail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);
            var B1_mail_40_data_in= all_mail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);
            var B1_mail_50_data_in= all_mail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);    
            var B1_mail_60_data_in= all_mail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);
            var B1_femail_10_data_in= all_femail_max_int_arr_in.filter(x => x.age < 20);      
            var B1_femail_20_data_in= all_femail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);      
            var B1_femail_30_data_in= all_femail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);  
            var B1_femail_40_data_in= all_femail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);  
            var B1_femail_50_data_in= all_femail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);       
            var B1_femail_60_data_in= all_femail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);

            var B1_10_data=[B1_mail_10_data_in.length,B1_femail_10_data_in.length];
            var B1_20_data=[B1_mail_20_data_in.length,B1_femail_20_data_in.length];
            var B1_30_data=[B1_mail_30_data_in.length,B1_femail_30_data_in.length];
            var B1_40_data=[B1_mail_40_data_in.length,B1_femail_40_data_in.length];
            var B1_50_data=[B1_mail_50_data_in.length,B1_femail_50_data_in.length];
            var B1_60_data=[B1_mail_60_data_in.length,B1_femail_60_data_in.length];
            //B2
            var B2_mail_10_data=[];
            var B2_mail_20_data=[];
            var B2_mail_30_data=[];
            var B2_mail_40_data=[];
            var B2_mail_50_data=[];
            var B2_mail_60_data=[];
            var B2_femail_10_data=[];
            var B2_femail_20_data=[];
            var B2_femail_30_data=[];
            var B2_femail_40_data=[];
            var B2_femail_50_data=[];
            var B2_femail_60_data=[];

            var B2_mail_10_data_in= all_mail_max_int_arr_in.filter(x => x.age < 20);           
            var B2_mail_20_data_in= all_mail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);           
            var B2_mail_30_data_in= all_mail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);       
            var B2_mail_40_data_in= all_mail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);       
            var B2_mail_50_data_in= all_mail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);            
            var B2_mail_60_data_in= all_mail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);      
            var B2_femail_10_data_in= all_femail_max_int_arr_in.filter(x => x.age < 20);            
            var B2_femail_20_data_in= all_femail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);            
            var B2_femail_30_data_in= all_femail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);        
            var B2_femail_40_data_in= all_femail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);        
            var B2_femail_50_data_in= all_femail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);             
            var B2_femail_60_data_in= all_femail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);   

            var B2_10_data=[B2_mail_10_data_in.length,B2_femail_10_data_in.length];
            var B2_20_data=[B2_mail_20_data_in.length,B2_femail_20_data_in.length];
            var B2_30_data=[B2_mail_30_data_in.length,B2_femail_30_data_in.length];
            var B2_40_data=[B2_mail_40_data_in.length,B2_femail_40_data_in.length];
            var B2_50_data=[B2_mail_50_data_in.length,B2_femail_50_data_in.length];
            var B2_60_data=[B2_mail_60_data_in.length,B2_femail_60_data_in.length];

        
            //D11
            
            var D11_10_data=[];
            var D11_20_data=[];
            var D11_30_data=[];
            var D11_40_data=[];
            var D11_50_data=[];
            var D11_60_data=[];
            for(let i=0 ;i<31 ;i=i+1){
            
                var D11_10_data_in= max_int_arr[i].filter(x => x.age < 20);
                D11_10_data.push(D11_10_data_in.length);
                
                var D11_20_data_in= max_int_arr[i].filter(x => x.age < 30 && x.age>=20);
                D11_20_data.push(D11_20_data_in.length);
                
                var D11_30_data_in= max_int_arr[i].filter(x => x.age < 40 && x.age>=30);
                D11_30_data.push(D11_30_data_in.length);
            
                var D11_40_data_in= max_int_arr[i].filter(x => x.age < 50 && x.age>=40);
                D11_40_data.push(D11_40_data_in.length);
            
                var D11_50_data_in= max_int_arr[i].filter(x => x.age < 60 && x.age>=50);
                D11_50_data.push(D11_50_data_in.length);
                
                var D11_60_data_in= max_int_arr[i].filter(x => x.age <= 120 && x.age>=60);
                D11_60_data.push(D11_60_data_in.length);
                
            }
            
        
            //D12
            var D12_10_data=[];
            var D12_20_data=[];
            var D12_30_data=[];
            var D12_40_data=[];
            var D12_50_data=[];
            var D12_60_data=[];
            
            for(let i=0 ;i<31 ;i=i+1){
        
            var D12_10_data_in= mail_max_int_arr[i].filter(x => x.age < 20);                D12_10_data.push(D12_10_data_in.length);
            
            var D12_20_data_in= mail_max_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D12_20_data.push(D12_20_data_in.length);
            
            var D12_30_data_in= mail_max_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D12_30_data.push(D12_30_data_in.length);
        
            var D12_40_data_in= mail_max_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D12_40_data.push(D12_40_data_in.length);
        
            var D12_50_data_in= mail_max_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D12_50_data.push(D12_50_data_in.length);
            
            var D12_60_data_in= mail_max_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D12_60_data.push(D12_60_data_in.length);
        
            }
        
            //D13
            
            var D13_10_data=[];
            var D13_20_data=[];
            var D13_30_data=[];
            var D13_40_data=[];
            var D13_50_data=[];
            var D13_60_data=[];
        
            for(let i=0 ;i<31 ;i=i+1){
        
            var D13_10_data_in= femail_max_int_arr[i].filter(x => x.age < 20);                D13_10_data.push(D13_10_data_in.length);
            
            var D13_20_data_in= femail_max_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D13_20_data.push(D13_20_data_in.length);
            
            var D13_30_data_in= femail_max_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D13_30_data.push(D13_30_data_in.length);
        
            var D13_40_data_in= femail_max_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D13_40_data.push(D13_40_data_in.length);
        
            var D13_50_data_in= femail_max_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D13_50_data.push(D13_50_data_in.length);
            
            var D13_60_data_in= femail_max_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D13_60_data.push(D13_60_data_in.length);
        
            }
            
        
            //D21
            
            
            var D21_10_data=[];
            var D21_20_data=[];
            var D21_30_data=[];
            var D21_40_data=[];
            var D21_50_data=[];
            var D21_60_data=[];
            for(let i=0 ;i<31 ;i=i+1){
            
                var D21_10_data_in= all_int_arr[i].filter(x => x.age < 20);                D21_10_data.push(D21_10_data_in.length);
                
                var D21_20_data_in= all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D21_20_data.push(D21_20_data_in.length);
                
                var D21_30_data_in= all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D21_30_data.push(D21_30_data_in.length);
            
                var D21_40_data_in= all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D21_40_data.push(D21_40_data_in.length);
            
                var D21_50_data_in= all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D21_50_data.push(D21_50_data_in.length);
                
                var D21_60_data_in= all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D21_60_data.push(D21_60_data_in.length);
                
        }
            
        
        
            //D22
            
            var D22_10_data=[];
            var D22_20_data=[];
            var D22_30_data=[];
            var D22_40_data=[];
            var D22_50_data=[];
            var D22_60_data=[];
        
            for(let i=0 ;i<31 ;i=i+1){
        
            var D22_10_data_in= mail_all_int_arr[i].filter(x => x.age < 20);                D22_10_data.push(D22_10_data_in.length);
            
            var D22_20_data_in= mail_all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D22_20_data.push(D22_20_data_in.length);
            
            var D22_30_data_in= mail_all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D22_30_data.push(D22_30_data_in.length);
        
            var D22_40_data_in= mail_all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D22_40_data.push(D22_40_data_in.length);
        
            var D22_50_data_in= mail_all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D22_50_data.push(D22_50_data_in.length);
            
            var D22_60_data_in= mail_all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D22_60_data.push(D22_60_data_in.length);
        
            }
        
        
            //D23
            var D23_10_data=[];
            var D23_20_data=[];
            var D23_30_data=[];
            var D23_40_data=[];
            var D23_50_data=[];
            var D23_60_data=[];
        
            for(let i=0 ;i<31 ;i=i+1){
        
            var D23_10_data_in= femail_all_int_arr[i].filter(x => x.age < 20);                D23_10_data.push(D23_10_data_in.length);
            
            var D23_20_data_in= femail_all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D23_20_data.push(D23_20_data_in.length);
            
            var D23_30_data_in= femail_all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D23_30_data.push(D23_30_data_in.length);
        
            var D23_40_data_in= femail_all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D23_40_data.push(D23_40_data_in.length);
        
            var D23_50_data_in= femail_all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D23_50_data.push(D23_50_data_in.length);
            
            var D23_60_data_in= femail_all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D23_60_data.push(D23_60_data_in.length);
        
            }
        }      
        
        //0～3時間の場合18プロット10分刻み
        else if(bet_time<10800 && bet_time>=0){
        
        
            //時間変化ラベル作成
            
            for(let h=0 ;h<user_outtime ;h=h+600){
                label_unix_in.push(user_intime+h)
            }
            
            var label_time_arr=[]//ラベル名
            
            
            
            for(let i=0 ;i<18 ;i=i+1){
                var label_time_in= new Date(label_unix_in[i]*1000);
                
                var label_time_in_2=label_time_in.getMonth()+1+"/"+label_time_in.getDate()+"/ "+label_time_in.getHours()+":"+label_time_in.getMinutes()
                
                label_time_arr.push(label_time_in_2);
            }
            
            
            
            //時間で分ける
            
            var backdata_arr_time=[];
            
            for(let i=0 ;i<10800 ;i=i+600){
                var backdata_arr_time_in= backdata_arr.filter(x => x.end_time_unix <= user_intime+(i+600) && x.end_time_unix > user_intime+i );
                backdata_arr_time.push(backdata_arr_time_in);
            }
            
            
            //関心度で分ける
            var int_line=70
            
            
            var all_max_int_arr  = backdata_arr.filter(x => x.interested <=100 && x.interested>=int_line );
        
        
            var all_nomal_int_arr= backdata_arr.filter(x => x.interested <int_line && x.interested>0 );
        
        
            var all_all_int_arr  = backdata_arr.filter(x => x.interested <=100 && x.interested>0 );
        
        
            var all_not_int_arr  = backdata_arr.filter(x => x.interested ===0 );
            
            
            
            
            
            var max_int_arr=[];
            var nomal_int_arr=[];
            var all_int_arr=[];
            var not_int_arr=[];
            
            
            for(let i=0 ;i<18 ;i=i+1){
                var max_int_arr_in= backdata_arr_time[i].filter(x => x.interested <=100 && x.interested>=int_line );
                max_int_arr.push(max_int_arr_in);
            }
            for(let i=0 ;i<18 ;i=i+1){
                var nomal_int_arr_in= backdata_arr_time[i].filter(x => x.interested <int_line && x.interested>0 );
                nomal_int_arr.push(nomal_int_arr_in);
            }
            for(let i=0 ;i<18 ;i=i+1){
                var all_int_arr_in= backdata_arr_time[i].filter(x => x.interested <=100 && x.interested>0 );
                all_int_arr.push(all_int_arr_in);
            }
            for(let i=0 ;i<18 ;i=i+1){
                var not_int_arr_in= backdata_arr_time[i].filter(x => x.interested ===0 );
                not_int_arr.push(not_int_arr_in);
            }
            
            //性別で分ける
            
            var all_mail_max_int_arr_in= all_max_int_arr.filter(x => x.gender === 1);
            var all_femail_max_int_arr_in= all_max_int_arr.filter(x => x.gender === 0);
            var all_mail_all_int_arr_in= all_all_int_arr.filter(x => x.gender === 1);
            var all_femail_all_int_arr_in= all_all_int_arr.filter(x => x.gender === 0);
            
            
            
            var mail_max_int_arr=[];
            var femail_max_int_arr=[];
            
            var femail_all_int_arr=[];
            var mail_all_int_arr=[];
            
            for(let i=0 ;i<18 ;i=i+1){
                var mail_max_int_arr_in= max_int_arr[i].filter(x => x.gender === 1);
                mail_max_int_arr.push(mail_max_int_arr_in);
                
                var femail_max_int_arr_in= max_int_arr[i].filter(x => x.gender === 0);
                femail_max_int_arr.push(femail_max_int_arr_in);
            }
            
            for(let i=0 ;i<18 ;i=i+1){
                var mail_all_int_arr_in= all_int_arr[i].filter(x => x.gender === 1);
                mail_all_int_arr.push(mail_all_int_arr_in);
                
                var femail_all_int_arr_in= all_int_arr[i].filter(x => x.gender === 0);
                femail_all_int_arr.push(femail_all_int_arr_in);
            }
            
            
            
            
            //A1
            var A1_data=[all_max_int_arr  .length, all_nomal_int_arr.length , all_not_int_arr  .length]
            
            //A21
            var A21_data=[all_mail_max_int_arr_in.length ,all_femail_max_int_arr_in.length]
            
            //A22
            var A22_data=[all_mail_all_int_arr_in.length ,all_femail_all_int_arr_in.length]
            
            //B1
            var B1_data=[all_mail_all_int_arr_in.length ,all_femail_all_int_arr_in.length]
            
            //C1
            var C1_maxint_data=[];
            var C1_nomalint_data=[];
            var C1_notint_data=[];
            
            for(let i=0;i<18;i++){
                C1_maxint_data.push(max_int_arr[i].length);
                C1_nomalint_data.push(nomal_int_arr[i].length);
                C1_notint_data.push(not_int_arr[i].length);
            }
            
            //B1
            var B1_mail_10_data=[];
            var B1_mail_20_data=[];
            var B1_mail_30_data=[];
            var B1_mail_40_data=[];
            var B1_mail_50_data=[];
            var B1_mail_60_data=[];
            var B1_femail_10_data=[];
            var B1_femail_20_data=[];
            var B1_femail_30_data=[];
            var B1_femail_40_data=[];
            var B1_femail_50_data=[];
            var B1_femail_60_data=[];

            var B1_mail_10_data_in= all_mail_max_int_arr_in.filter(x => x.age < 20);    
            var B1_mail_20_data_in= all_mail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);    
            var B1_mail_30_data_in= all_mail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);
            var B1_mail_40_data_in= all_mail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);
            var B1_mail_50_data_in= all_mail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);    
            var B1_mail_60_data_in= all_mail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);
            var B1_femail_10_data_in= all_femail_max_int_arr_in.filter(x => x.age < 20);      
            var B1_femail_20_data_in= all_femail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);      
            var B1_femail_30_data_in= all_femail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);  
            var B1_femail_40_data_in= all_femail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);  
            var B1_femail_50_data_in= all_femail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);       
            var B1_femail_60_data_in= all_femail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);

            var B1_10_data=[B1_mail_10_data_in.length,B1_femail_10_data_in.length];
            var B1_20_data=[B1_mail_20_data_in.length,B1_femail_20_data_in.length];
            var B1_30_data=[B1_mail_30_data_in.length,B1_femail_30_data_in.length];
            var B1_40_data=[B1_mail_40_data_in.length,B1_femail_40_data_in.length];
            var B1_50_data=[B1_mail_50_data_in.length,B1_femail_50_data_in.length];
            var B1_60_data=[B1_mail_60_data_in.length,B1_femail_60_data_in.length];
            
            //B2
            var B2_mail_10_data=[];
            var B2_mail_20_data=[];
            var B2_mail_30_data=[];
            var B2_mail_40_data=[];
            var B2_mail_50_data=[];
            var B2_mail_60_data=[];
            var B2_femail_10_data=[];
            var B2_femail_20_data=[];
            var B2_femail_30_data=[];
            var B2_femail_40_data=[];
            var B2_femail_50_data=[];
            var B2_femail_60_data=[];

            var B2_mail_10_data_in= all_mail_max_int_arr_in.filter(x => x.age < 20);           
            var B2_mail_20_data_in= all_mail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);           
            var B2_mail_30_data_in= all_mail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);       
            var B2_mail_40_data_in= all_mail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);       
            var B2_mail_50_data_in= all_mail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);            
            var B2_mail_60_data_in= all_mail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);      
            var B2_femail_10_data_in= all_femail_max_int_arr_in.filter(x => x.age < 20);            
            var B2_femail_20_data_in= all_femail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);            
            var B2_femail_30_data_in= all_femail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);        
            var B2_femail_40_data_in= all_femail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);        
            var B2_femail_50_data_in= all_femail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);             
            var B2_femail_60_data_in= all_femail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);   

            var B2_10_data=[B2_mail_10_data_in.length,B2_femail_10_data_in.length];
            var B2_20_data=[B2_mail_20_data_in.length,B2_femail_20_data_in.length];
            var B2_30_data=[B2_mail_30_data_in.length,B2_femail_30_data_in.length];
            var B2_40_data=[B2_mail_40_data_in.length,B2_femail_40_data_in.length];
            var B2_50_data=[B2_mail_50_data_in.length,B2_femail_50_data_in.length];
            var B2_60_data=[B2_mail_60_data_in.length,B2_femail_60_data_in.length];

        
            
            //D11
            
            var D11_10_data=[];
            var D11_20_data=[];
            var D11_30_data=[];
            var D11_40_data=[];
            var D11_50_data=[];
            var D11_60_data=[];
            for(let i=0 ;i<18 ;i=i+1){
            
                var D11_10_data_in= max_int_arr[i].filter(x => x.age < 20);
                D11_10_data.push(D11_10_data_in.length);
                
                var D11_20_data_in= max_int_arr[i].filter(x => x.age < 30 && x.age>=20);
                D11_20_data.push(D11_20_data_in.length);
                
                var D11_30_data_in= max_int_arr[i].filter(x => x.age < 40 && x.age>=30);
                D11_30_data.push(D11_30_data_in.length);
            
                var D11_40_data_in= max_int_arr[i].filter(x => x.age < 50 && x.age>=40);
                D11_40_data.push(D11_40_data_in.length);
            
                var D11_50_data_in= max_int_arr[i].filter(x => x.age < 60 && x.age>=50);
                D11_50_data.push(D11_50_data_in.length);
                
                var D11_60_data_in= max_int_arr[i].filter(x => x.age <= 120 && x.age>=60);
                D11_60_data.push(D11_60_data_in.length);
                
            }
                
            
            //D12
            var D12_10_data=[];
            var D12_20_data=[];
            var D12_30_data=[];
            var D12_40_data=[];
            var D12_50_data=[];
            var D12_60_data=[];
            
            for(let i=0 ;i<18 ;i=i+1){
            
                var D12_10_data_in= mail_max_int_arr[i].filter(x => x.age < 20);                D12_10_data.push(D12_10_data_in.length);
                
                var D12_20_data_in= mail_max_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D12_20_data.push(D12_20_data_in.length);
                
                var D12_30_data_in= mail_max_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D12_30_data.push(D12_30_data_in.length);
            
                var D12_40_data_in= mail_max_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D12_40_data.push(D12_40_data_in.length);
            
                var D12_50_data_in= mail_max_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D12_50_data.push(D12_50_data_in.length);
                
                var D12_60_data_in= mail_max_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D12_60_data.push(D12_60_data_in.length);
            
            }
            
            //D13
            
            var D13_10_data=[];
            var D13_20_data=[];
            var D13_30_data=[];
            var D13_40_data=[];
            var D13_50_data=[];
            var D13_60_data=[];
            
            for(let i=0 ;i<18 ;i=i+1){
            
                var D13_10_data_in= femail_max_int_arr[i].filter(x => x.age < 20);                D13_10_data.push(D13_10_data_in.length);
                
                var D13_20_data_in= femail_max_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D13_20_data.push(D13_20_data_in.length);
                
                var D13_30_data_in= femail_max_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D13_30_data.push(D13_30_data_in.length);
            
                var D13_40_data_in= femail_max_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D13_40_data.push(D13_40_data_in.length);
            
                var D13_50_data_in= femail_max_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D13_50_data.push(D13_50_data_in.length);
                
                var D13_60_data_in= femail_max_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D13_60_data.push(D13_60_data_in.length);
            
            }
                
            
            //D21
            
            
            var D21_10_data=[];
            var D21_20_data=[];
            var D21_30_data=[];
            var D21_40_data=[];
            var D21_50_data=[];
            var D21_60_data=[];
            for(let i=0 ;i<18 ;i=i+1){
            
                var D21_10_data_in= all_int_arr[i].filter(x => x.age < 20);                D21_10_data.push(D21_10_data_in.length);
                
                var D21_20_data_in= all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D21_20_data.push(D21_20_data_in.length);
                
                var D21_30_data_in= all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D21_30_data.push(D21_30_data_in.length);
            
                var D21_40_data_in= all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D21_40_data.push(D21_40_data_in.length);
            
                var D21_50_data_in= all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D21_50_data.push(D21_50_data_in.length);
                
                var D21_60_data_in= all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D21_60_data.push(D21_60_data_in.length);
                
            }
                
            
            
            //D22
            
            var D22_10_data=[];
            var D22_20_data=[];
            var D22_30_data=[];
            var D22_40_data=[];
            var D22_50_data=[];
            var D22_60_data=[];
            
            for(let i=0 ;i<18 ;i=i+1){
            
                var D22_10_data_in= mail_all_int_arr[i].filter(x => x.age < 20);                D22_10_data.push(D22_10_data_in.length);
                
                var D22_20_data_in= mail_all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D22_20_data.push(D22_20_data_in.length);
                
                var D22_30_data_in= mail_all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D22_30_data.push(D22_30_data_in.length);
            
                var D22_40_data_in= mail_all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D22_40_data.push(D22_40_data_in.length);
            
                var D22_50_data_in= mail_all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D22_50_data.push(D22_50_data_in.length);
                
                var D22_60_data_in= mail_all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D22_60_data.push(D22_60_data_in.length);
            
            }
            
            
            //D23
            var D23_10_data=[];
            var D23_20_data=[];
            var D23_30_data=[];
            var D23_40_data=[];
            var D23_50_data=[];
            var D23_60_data=[];
            
            for(let i=0 ;i<18 ;i=i+1){
        
            var D23_10_data_in= femail_all_int_arr[i].filter(x => x.age < 20);                D23_10_data.push(D23_10_data_in.length);
            
            var D23_20_data_in= femail_all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D23_20_data.push(D23_20_data_in.length);
            
            var D23_30_data_in= femail_all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D23_30_data.push(D23_30_data_in.length);
        
            var D23_40_data_in= femail_all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D23_40_data.push(D23_40_data_in.length);
        
            var D23_50_data_in= femail_all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D23_50_data.push(D23_50_data_in.length);
            
            var D23_60_data_in= femail_all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D23_60_data.push(D23_60_data_in.length);
        
            }
                
        }
        
        
        //3時間から1日 
        else if (bet_time<86400 && bet_time>=10800){
        
            //時間変化ラベル作成

            for(let h=0 ;h<user_outtime ;h=h+3600){
                label_unix_in.push(user_intime+h)
            }

            var label_time_arr=[]//ラベル名
                
                
                
            for(let i=0 ;i<21 ;i=i+1){
                var label_time_in= new Date(label_unix_in[i]*1000);
                
                var label_time_in_2=label_time_in.getMonth()+1+"/"+label_time_in.getDate()+"/ "+label_time_in.getHours()+":"+label_time_in.getMinutes()
                
                    label_time_arr.push(label_time_in_2);
            }
            
            
            
            //時間で分ける
            
            var backdata_arr_time=[];
            
            for(let i=0 ;i<86400 ;i=i+10800){
                var backdata_arr_time_in= backdata_arr.filter(x => x.end_time_unix <= user_intime+(i+3600) && x.end_time_unix > user_intime+i );
                backdata_arr_time.push(backdata_arr_time_in);
            }
            
            
            //関心度で分ける
            var int_line=70
            
            
                var all_max_int_arr  = backdata_arr.filter(x => x.interested <=100 && x.interested>=int_line );
            
            
                var all_nomal_int_arr= backdata_arr.filter(x => x.interested <int_line && x.interested>0 );
            
            
                var all_all_int_arr  = backdata_arr.filter(x => x.interested <=100 && x.interested>0 );
            
            
                var all_not_int_arr  = backdata_arr.filter(x => x.interested ===0 );
            
            
            
            
            
            var max_int_arr=[];
            var nomal_int_arr=[];
            var all_int_arr=[];
            var not_int_arr=[];
                
                
            for(let i=0 ;i<21 ;i=i+1){
                var max_int_arr_in= backdata_arr_time[i].filter(x => x.interested <=100 && x.interested>=int_line );
                max_int_arr.push(max_int_arr_in);
            }
            for(let i=0 ;i<21 ;i=i+1){
                var nomal_int_arr_in= backdata_arr_time[i].filter(x => x.interested <int_line && x.interested>0 );
                nomal_int_arr.push(nomal_int_arr_in);
            }
            for(let i=0 ;i<21 ;i=i+1){
                var all_int_arr_in= backdata_arr_time[i].filter(x => x.interested <=100 && x.interested>0 );
                all_int_arr.push(all_int_arr_in);
            }
            for(let i=0 ;i<21 ;i=i+1){
                var not_int_arr_in= backdata_arr_time[i].filter(x => x.interested ===0 );
                not_int_arr.push(not_int_arr_in);
            }
                
                //性別で分ける
                
                var all_mail_max_int_arr_in=   all_max_int_arr.filter(x => x.gender === 1);
                var all_femail_max_int_arr_in= all_max_int_arr.filter(x => x.gender === 0);
                var all_mail_all_int_arr_in=   all_all_int_arr.filter(x => x.gender === 1);
                var all_femail_all_int_arr_in= all_all_int_arr.filter(x => x.gender === 0);
                
                
                
                var mail_max_int_arr=[];
                var femail_max_int_arr=[];
                
                var femail_all_int_arr=[];
                var mail_all_int_arr=[];
                
                for(let i=0 ;i<21 ;i=i+1){
                var mail_max_int_arr_in= max_int_arr[i].filter(x => x.gender === 1);
                mail_max_int_arr.push(mail_max_int_arr_in);
                
                var femail_max_int_arr_in= max_int_arr[i].filter(x => x.gender === 0);
                femail_max_int_arr.push(femail_max_int_arr_in);
                }
                
                for(let i=0 ;i<21 ;i=i+1){
                var mail_all_int_arr_in= all_int_arr[i].filter(x => x.gender === 1);
                mail_all_int_arr.push(mail_all_int_arr_in);
                
                var femail_all_int_arr_in= all_int_arr[i].filter(x => x.gender === 0);
                femail_all_int_arr.push(femail_all_int_arr_in);
                }
                
                
                
                
                //A1
                var A1_data=[all_max_int_arr  .length, all_nomal_int_arr.length , all_not_int_arr  .length]
                
                //A21
                var A21_data=[all_mail_max_int_arr_in.length ,all_femail_max_int_arr_in.length]
                
                //A22
                var A22_data=[all_mail_all_int_arr_in.length ,all_femail_all_int_arr_in.length]
                
            //B1
            var B1_mail_10_data=[];
            var B1_mail_20_data=[];
            var B1_mail_30_data=[];
            var B1_mail_40_data=[];
            var B1_mail_50_data=[];
            var B1_mail_60_data=[];
            var B1_femail_10_data=[];
            var B1_femail_20_data=[];
            var B1_femail_30_data=[];
            var B1_femail_40_data=[];
            var B1_femail_50_data=[];
            var B1_femail_60_data=[];

            var B1_mail_10_data_in= all_mail_max_int_arr_in.filter(x => x.age < 20);    
            var B1_mail_20_data_in= all_mail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);    
            var B1_mail_30_data_in= all_mail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);
            var B1_mail_40_data_in= all_mail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);
            var B1_mail_50_data_in= all_mail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);    
            var B1_mail_60_data_in= all_mail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);
            var B1_femail_10_data_in= all_femail_max_int_arr_in.filter(x => x.age < 20);      
            var B1_femail_20_data_in= all_femail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);      
            var B1_femail_30_data_in= all_femail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);  
            var B1_femail_40_data_in= all_femail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);  
            var B1_femail_50_data_in= all_femail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);       
            var B1_femail_60_data_in= all_femail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);

            var B1_10_data=[B1_mail_10_data_in.length,B1_femail_10_data_in.length];
            var B1_20_data=[B1_mail_20_data_in.length,B1_femail_20_data_in.length];
            var B1_30_data=[B1_mail_30_data_in.length,B1_femail_30_data_in.length];
            var B1_40_data=[B1_mail_40_data_in.length,B1_femail_40_data_in.length];
            var B1_50_data=[B1_mail_50_data_in.length,B1_femail_50_data_in.length];
            var B1_60_data=[B1_mail_60_data_in.length,B1_femail_60_data_in.length];
            
            //B2
            var B2_mail_10_data=[];
            var B2_mail_20_data=[];
            var B2_mail_30_data=[];
            var B2_mail_40_data=[];
            var B2_mail_50_data=[];
            var B2_mail_60_data=[];
            var B2_femail_10_data=[];
            var B2_femail_20_data=[];
            var B2_femail_30_data=[];
            var B2_femail_40_data=[];
            var B2_femail_50_data=[];
            var B2_femail_60_data=[];

            var B2_mail_10_data_in= all_mail_max_int_arr_in.filter(x => x.age < 20);           
            var B2_mail_20_data_in= all_mail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);           
            var B2_mail_30_data_in= all_mail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);       
            var B2_mail_40_data_in= all_mail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);       
            var B2_mail_50_data_in= all_mail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);            
            var B2_mail_60_data_in= all_mail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);      
            var B2_femail_10_data_in= all_femail_max_int_arr_in.filter(x => x.age < 20);            
            var B2_femail_20_data_in= all_femail_max_int_arr_in.filter(x => x.age < 30 && x.age>=20);            
            var B2_femail_30_data_in= all_femail_max_int_arr_in.filter(x => x.age < 40 && x.age>=30);        
            var B2_femail_40_data_in= all_femail_max_int_arr_in.filter(x => x.age < 50 && x.age>=40);        
            var B2_femail_50_data_in= all_femail_max_int_arr_in.filter(x => x.age < 60 && x.age>=50);             
            var B2_femail_60_data_in= all_femail_max_int_arr_in.filter(x => x.age <= 120 && x.age>=60);   

            var B2_10_data=[B2_mail_10_data_in.length,B2_femail_10_data_in.length];
            var B2_20_data=[B2_mail_20_data_in.length,B2_femail_20_data_in.length];
            var B2_30_data=[B2_mail_30_data_in.length,B2_femail_30_data_in.length];
            var B2_40_data=[B2_mail_40_data_in.length,B2_femail_40_data_in.length];
            var B2_50_data=[B2_mail_50_data_in.length,B2_femail_50_data_in.length];
            var B2_60_data=[B2_mail_60_data_in.length,B2_femail_60_data_in.length];
        
                //C1
                var C1_maxint_data=[];
                var C1_nomalint_data=[];
                var C1_notint_data=[];
                
                for(let i=0;i<21;i++){
                C1_maxint_data.push(max_int_arr[i].length);
                C1_nomalint_data.push(nomal_int_arr[i].length);
                C1_notint_data.push(not_int_arr[i].length);
                }
                
                
                
                
                //D11
                
                var D11_10_data=[];
                var D11_20_data=[];
                var D11_30_data=[];
                var D11_40_data=[];
                var D11_50_data=[];
                var D11_60_data=[];
                for(let i=0 ;i<21 ;i=i+1){
                
                    var D11_10_data_in= max_int_arr[i].filter(x => x.age < 20);
                    D11_10_data.push(D11_10_data_in.length);
                    
                    var D11_20_data_in= max_int_arr[i].filter(x => x.age < 30 && x.age>=20);
                    D11_20_data.push(D11_20_data_in.length);
                    
                    var D11_30_data_in= max_int_arr[i].filter(x => x.age < 40 && x.age>=30);
                    D11_30_data.push(D11_30_data_in.length);
                
                    var D11_40_data_in= max_int_arr[i].filter(x => x.age < 50 && x.age>=40);
                    D11_40_data.push(D11_40_data_in.length);
                
                    var D11_50_data_in= max_int_arr[i].filter(x => x.age < 60 && x.age>=50);
                    D11_50_data.push(D11_50_data_in.length);
                    
                    var D11_60_data_in= max_int_arr[i].filter(x => x.age <= 120 && x.age>=60);
                    D11_60_data.push(D11_60_data_in.length);
                    
                }
                    
                
                //D12
                var D12_10_data=[];
                var D12_20_data=[];
                var D12_30_data=[];
                var D12_40_data=[];
                var D12_50_data=[];
                var D12_60_data=[];
                
                    for(let i=0 ;i<21 ;i=i+1){
                
                    var D12_10_data_in= mail_max_int_arr[i].filter(x => x.age < 20);                D12_10_data.push(D12_10_data_in.length);
                    
                    var D12_20_data_in= mail_max_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D12_20_data.push(D12_20_data_in.length);
                    
                    var D12_30_data_in= mail_max_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D12_30_data.push(D12_30_data_in.length);
                
                    var D12_40_data_in= mail_max_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D12_40_data.push(D12_40_data_in.length);
                
                    var D12_50_data_in= mail_max_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D12_50_data.push(D12_50_data_in.length);
                    
                    var D12_60_data_in= mail_max_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D12_60_data.push(D12_60_data_in.length);
                
                    }
                
                //D13
                
                var D13_10_data=[];
                var D13_20_data=[];
                var D13_30_data=[];
                var D13_40_data=[];
                var D13_50_data=[];
                var D13_60_data=[];
                
                    for(let i=0 ;i<21 ;i=i+1){
                
                    var D13_10_data_in= femail_max_int_arr[i].filter(x => x.age < 20);                D13_10_data.push(D13_10_data_in.length);
                    
                    var D13_20_data_in= femail_max_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D13_20_data.push(D13_20_data_in.length);
                    
                    var D13_30_data_in= femail_max_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D13_30_data.push(D13_30_data_in.length);
                
                    var D13_40_data_in= femail_max_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D13_40_data.push(D13_40_data_in.length);
                
                    var D13_50_data_in= femail_max_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D13_50_data.push(D13_50_data_in.length);
                    
                    var D13_60_data_in= femail_max_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D13_60_data.push(D13_60_data_in.length);
                
                    }
                    
                
                //D21
                var D21_10_data=[];
                var D21_20_data=[];
                var D21_30_data=[];
                var D21_40_data=[];
                var D21_50_data=[];
                var D21_60_data=[];
                for(let i=0 ;i<21 ;i=i+1){
                
                    var D21_10_data_in= all_int_arr[i].filter(x => x.age < 20);                D21_10_data.push(D21_10_data_in.length);
                    
                    var D21_20_data_in= all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D21_20_data.push(D21_20_data_in.length);
                    
                    var D21_30_data_in= all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D21_30_data.push(D21_30_data_in.length);
                
                    var D21_40_data_in= all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D21_40_data.push(D21_40_data_in.length);
                
                    var D21_50_data_in= all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D21_50_data.push(D21_50_data_in.length);
                    
                    var D21_60_data_in= all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D21_60_data.push(D21_60_data_in.length);
                    
                }
                    
                
                
                //D22
                
                var D22_10_data=[];
                var D22_20_data=[];
                var D22_30_data=[];
                var D22_40_data=[];
                var D22_50_data=[];
                var D22_60_data=[];
                
                for(let i=0 ;i<21 ;i=i+1){
            
                var D22_10_data_in= mail_all_int_arr[i].filter(x => x.age < 20);                D22_10_data.push(D22_10_data_in.length);
                
                var D22_20_data_in= mail_all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D22_20_data.push(D22_20_data_in.length);
                
                var D22_30_data_in= mail_all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D22_30_data.push(D22_30_data_in.length);
            
                var D22_40_data_in= mail_all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D22_40_data.push(D22_40_data_in.length);
            
                var D22_50_data_in= mail_all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D22_50_data.push(D22_50_data_in.length);
                
                var D22_60_data_in= mail_all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D22_60_data.push(D22_60_data_in.length);
            
                }
                
                
                //D23
                var D23_10_data=[];
                var D23_20_data=[];
                var D23_30_data=[];
                var D23_40_data=[];
                var D23_50_data=[];
                var D23_60_data=[];
                
                for(let i=0 ;i<21 ;i=i+1){
            
                var D23_10_data_in= femail_all_int_arr[i].filter(x => x.age < 20);                D23_10_data.push(D23_10_data_in.length);
                
                var D23_20_data_in= femail_all_int_arr[i].filter(x => x.age < 30 && x.age>=20);   D23_20_data.push(D23_20_data_in.length);
                
                var D23_30_data_in= femail_all_int_arr[i].filter(x => x.age < 40 && x.age>=30);   D23_30_data.push(D23_30_data_in.length);
            
                var D23_40_data_in= femail_all_int_arr[i].filter(x => x.age < 50 && x.age>=40);   D23_40_data.push(D23_40_data_in.length);
            
                var D23_50_data_in= femail_all_int_arr[i].filter(x => x.age < 60 && x.age>=50);   D23_50_data.push(D23_50_data_in.length);
                
                var D23_60_data_in= femail_all_int_arr[i].filter(x => x.age <= 120 && x.age>=60); D23_60_data.push(D23_60_data_in.length);
            
                }
                    
            };
        
            //console.log(label_time_arr)

            this.A1_data = A1_data;
            this.A21_data = A21_data;
            this.A22_data = A22_data;
            this.B1_10_data = B1_10_data;
            this.B1_20_data = B1_20_data;
            this.B1_30_data = B1_30_data;
            this.B1_40_data = B1_40_data;
            this.B1_50_data = B1_50_data;
            this.B1_60_data = B1_60_data;
            this.B2_10_data = B2_10_data;
            this.B2_20_data = B2_20_data;
            this.B2_30_data = B2_30_data;
            this.B2_40_data = B2_40_data;
            this.B2_50_data = B2_50_data;
            this.B2_60_data = B2_60_data;
            this.label_time_arr = label_time_arr;
            this.C1_maxint_data= C1_maxint_data;
            this.C1_nomalint_data = C1_nomalint_data;
            this.C1_notint_data = C1_notint_data;
            this.D11_10_data = D11_10_data;
            this.D11_20_data = D11_20_data;
            this.D11_30_data = D11_30_data;
            this.D11_40_data = D11_40_data;
            this.D11_50_data = D11_50_data;
            this.D11_60_data = D11_60_data;
            this.D12_10_data = D12_10_data;
            this.D12_20_data = D12_20_data;
            this.D12_30_data = D12_30_data;
            this.D12_40_data = D12_40_data;
            this.D12_50_data = D12_50_data;
            this.D12_60_data = D12_60_data;
            this.D13_10_data = D13_10_data;
            this.D13_20_data = D13_20_data;
            this.D13_30_data = D13_30_data;
            this.D13_40_data = D13_40_data;
            this.D13_50_data = D13_50_data;
            this.D13_60_data = D13_60_data;
            this.D21_10_data = D21_10_data;
            this.D21_20_data = D21_20_data;
            this.D21_30_data = D21_30_data;
            this.D21_40_data = D21_40_data;
            this.D21_50_data = D21_50_data;
            this.D21_60_data = D21_60_data;
            this.D22_10_data = D22_10_data;
            this.D22_20_data = D22_20_data;
            this.D22_30_data = D22_30_data;
            this.D22_40_data = D22_40_data;
            this.D22_50_data = D22_50_data;
            this.D22_60_data = D22_60_data;
            this.D23_10_data = D23_10_data;
            this.D23_20_data = D23_20_data;
            this.D23_30_data = D23_30_data;
            this.D23_40_data = D23_40_data;
            this.D23_50_data = D23_50_data;
            this.D23_60_data = D23_60_data;
    }

    
    
}