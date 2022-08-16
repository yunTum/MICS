<template>


             <div class="graphA">
                <div class="graphA1">
                    <div class="graphA1title">
                        <h1>関心度別人数比</h1>
                        
                    </div>
                    <hr noshade>    
                    <div class="graphA1inner">
                        <glaph_A1/>
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
                            <glaph_A21/>
                        </div>
                        <div class="A22">
                            <h2>特に関心あり&関心あり</h2>
                           <glaph_A22/>
                        </div>
                    </div>
                </div>                     
            </div>


        <div class="graphB">
                <div class="graphBtitle">
                    <h1>関心度別男女年齢比</h1>
                    
                </div>
                <hr noshade> 
                <div class="B1">
                    <div class="B1h2"><h2>特に関心あり</h2></div>
                    <div class="B1inner"><glaph_B1  width="100" height="12"/></div>
                </div>
                <hr noshade> 
                <div class="B2">
                    <div class="B2h2">
                    <h2>特に関心あり</h2>
                    <h2>&</h2>
                    <h2>関心あり</h2>
                    </div>
                    <div class="B2inner"><glaph_B2  width="100" height="12"/></div>
                </div>
            </div>
  
              <div class="graphC">
                <div class="graphCtitle">
                    <h1>関心度時間推移</h1>
                    
                </div>
                <div><hr noshade></div>
                 
                <div class="C1"><glaph_C1  width="100" height="25"></glaph_C1></div>
            </div>

              <div class="graphD1">
                <div class="graphD1title">
                    <h1>【関心あり】年齢比時間推移</h1>
                    
                </div>
                <hr noshade> 
                <div class="graphD11">
                    <h2>全体</h2>
                    <div class="graphD11inner"><glaph_D11 width="100" height="20"/></div>
                </div>
                <hr>
                <div class="graphD12">
                    <h2>男性</h2>
                    <div class="graphD12inner"><glaph_D12 width="100" height="20"/></div>
                </div>
                <hr>
                <div class="graphD13">
                    <h2>女性</h2>
                    <div class="graphD13inner"><glaph_D13 width="100" height="20"/></div>
                </div>
            </div>
	
                <div class="graphD2">
                <div class="graphD2title">
                <h1>【特に関心あり】年齢比時間推移</h1>
                    
                </div>
                <hr noshade> 
                <div class="graphD21">
                    <h2>全体</h2>
                    <div class="graphD21inner"><glaph_D21 width="100" height="20"/></div>
                </div>
                <hr>
                <div class="graphD22">
                    <h2>男性</h2>
                    <div class="graphD22inner"><glaph_D22 width="100" height="20"/></div>
                </div>
                <hr>
                <div class="graphD23">
                    <h2>女性</h2>
                    <div class="graphD23inner"><glaph_D23 width="100" height="20"/></div>         
                 </div>
            </div>
  
  
</template>

<script>
import glaph_A1  from './glaph/glaph_A1'
import glaph_A21 from './glaph/glahp_A21'
import glaph_A22 from './glaph/glaph_A22'
import glaph_B1  from './glaph/glaph_B1'
import glaph_B2  from './glaph/glaph_B2'
import glaph_C1  from './glaph/glaph_C1'
import glaph_D11 from './glaph/glaph_D11'
import glaph_D12 from './glaph/glaph_D12'
import glaph_D13 from './glaph/glaph_D13'
import glaph_D21 from './glaph/glaph_D21'
import glaph_D22 from './glaph/glaph_D22'
import glaph_D23 from './glaph/glaph_D23'
//import test from '../../public/serch'


export default {
// Appでデータ入れるとき用

// data(){
//   return{
//     test_out:test
//   }
// },


 name: 'Plot_glaph',


  components: {
    glaph_A1,
    glaph_A21,
    glaph_A22,
    glaph_B1,
    glaph_B2,
    glaph_C1,
    glaph_D11,
    glaph_D12,
    glaph_D13,
    glaph_D21,
    glaph_D22,
    glaph_D23,
   
}
}
</script>

<style>
/* 
* {
    margin: 0;
  }

header{
    display:flex;
    width:100%;
    height:100px;
    background-color:rgb(241, 102, 9);
    align-items:center;
}
.logo img{
    height:80px;
    width:80px;
    margin-left: 25px;
    margin-top:10px;   
}
.help,a{
    text-decoration: none;
    color:white;
    margin-right: 20px;
    
}
.title{
    margin-right:auto;
    color: white;
}
.menugroup{
    display: flex;
}
.help{
    list-style: none;
    display:inline-block;
    margin-top:8px;
    margin-right: 13px;
    font-weight: bold;
}
.questionlogo{
    list-style:none;
    margin-top:7px;
}
.questionlogo img{
    height:25px;
    width:25px;
}

.container{
    background-color:whitesmoke; 
    height:4400px;
}
hr{
    border:solid 1px #e2e2e2;
    border-radius: 5px;
    width:93%;
}



.searcharea{
    width:70%;
    height:300px;
    margin:0 auto;
    background-color:white;
    border-radius:20px;
    position:relative;
    top:1.5%;  
    
    border-bottom: solid 5px #bdc0c3;
    border-left:solid 3px #bdc0c3 ;
    border-radius: 9px;
    padding: 0.5em 1em;
}
.inputarea{
    position:relative;
    margin:0 auto;
    width:80%;
    position:relative;
    top:20%;
    display:flex;   
}
.inputarea p{
    color:rgb(241, 102, 9);
    font-weight:900;
}
.searchbutton{
    height:20px;
    width:40%;
    position:relative;
    margin:0 auto;
    top:40%;
    text-align: center;
}
.searchbutton input{
    -webkit-appearance: none;
    border-color:rgb(241, 102, 9);
    border-radius:7px;
    border-width:medium;
    font-size: 16px;
    color:#8b8c8e;
    background-color:white;
    height:36px;
    width:40%;

    
}
.inputarea input{
    -webkit-appearance: none;
    border-color:rgb(241, 102, 9);
    border-radius:7px;
    border-width:medium;
    font-size: 16px;
    color:#8b8c8e;
    height:36px;
    width:400px;
}
.searcharea p{
    position:relative;
    bottom:0%;
}


.graphA h1{
    color:rgb(241, 102, 9);
}
.graphA{
    width:85%;
    height:400px;
    margin:0 auto;
    position:relative;
    top:3%;
    display:flex;
}
.graphA1{
    width:35%;
    height:400px;
    margin:0 auto;
   
    background-color: white;
    margin-right:40px;

    background: white;
    border-bottom: solid 5px #bdc0c3;
    border-left:solid 3px #bdc0c3 ;
    border-radius: 9px;
    padding: 0.5em 1em;
}
.graphA1title{
    display:flex;
}
.graphA1inner {
    width:70%;
    margin:0 auto;
    
}

.graphA2{
    width:65%;
    height:400px;
    margin:0 auto;
    
    background: white;
    border-bottom: solid 5px #bdc0c3;
    border-left:solid 3px #bdc0c3 ;
    border-radius: 9px;
    padding: 0.5em 1em;
}
.graphA2title{
    display:flex;
}
.graphA2inner {
    width:90%;
    margin:0 auto;
    display:flex;
}
.A21{
    width:40%;
    margin:0 auto;
}
.A22{
    width:40%;
    margin:0 auto;
}




.graphB{
    width:85%;
    height:400px;
    margin:0 auto;
    position:relative;
    top:5%;

    background: white;
    border-bottom: solid 5px #bdc0c3;
    border-left:solid 3px #bdc0c3 ;
    border-radius: 9px;
    padding: 0.5em 1em;
}
.graphBtitle{
    display:flex;
}
.B1{
    height:40%;
    margin:0 auto;
    display:flex;
}
.B1h2{
    margin:auto 0;
}
.B1inner{
    width:80%;
}

.B2{
    height:40%;
    margin:0 auto;
    display:flex;
}
.B2h2{
    margin:auto 0;
}
.B2inner{
    width:80%;
}



.graphC{
    width:85%;
    height:400px;
    margin:0 auto;
    position:relative;
    top:7%;

    background: white;
    border-bottom: solid 5px #bdc0c3;
    border-left:solid 3px #bdc0c3 ;
    border-radius: 9px;
    padding: 0.5em 1em;
}
.graphCtitle{
    display:flex;
}




.graphD1{
    width:85%;
    height:1100px;
    margin:0 auto;
    position:relative;
    top:9%;

    background: white;
    border-bottom: solid 5px #bdc0c3;
    border-left:solid 3px #bdc0c3 ;
    border-radius: 9px;
    padding: 0.5em 1em;
}
.graphD1title{
    display:flex;
}
.graphD11{
    height: 30%;
}
.graphD12{
    height: 30%;
}
.graphD13{
    height: 30%;
}





.graphD2{
    width:85%;
    height:1100px;
    margin:0 auto;
    position:relative;
    top:11%;

    background: white;
    border-bottom: solid 5px #bdc0c3;
    border-left:solid 3px #bdc0c3 ;
    border-radius: 9px;
    padding: 0.5em 1em;
}
.graphD2title{
    display:flex;
}
.graphD21{
    height: 30%;
}
.graphD22{
    height: 30%;
}
.graphD23{
    height: 30%;
}


footer{
    display:flex;
    width:100%;
    height:200px;
    background-color:rgb(19, 20, 51);
    align-items:center;
}
.footertitle{
    
    margin-left:2%;
    margin-right: auto;
    color: white;
} */

</style>