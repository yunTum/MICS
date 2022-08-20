/*
MICS Front
class関連
*/

class MICS{
    //コンストラクタ
    constructor() {
        this.date_first = -1;
        this.date_last = -1;
        this.interest_data = [];
        this.is_pulled = false;
        this.container = document.getElementById("serch_container");
    }
    
    //サーバーからデータ取得
    GetMessage(date_first, date_last, interest_data){
        if(interest_data != '[]'){
            if(this.is_pulled == false){
                this.date_first = date_first;
                this.date_last = date_last;
                this.interest_data = interest_data;
                console.log("[Info] Successfully input data into MICS class");
                this.is_pulled = true;
                this.container.style.height = 4400 + "px";
                this.container.style.paddingTop = 0 + "px";
                this.graph = new MICSGrahp(this);
            }else{
                console.log("[Info] Successfully updated MICS class");
                this.date_first = date_first;
                this.date_last = date_last;
                this.interest_data = interest_data;
                this.graph.Update(this);
            }
        }
    }

    //サーバーからデータを取得(ラッパー)
    PullMessage(){
        PullMessage(this)
    }

}

mics_data = new MICS();