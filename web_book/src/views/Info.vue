<template>
    <div class="box" :style="big_box" @touchstart="touch_wz">
        <v-progress-linear fixed top indeterminate color="light-blue" v-if="loading"></v-progress-linear>
        <div class="contents m-auto mt-24 shadow-2xl w-1/2" :style="{background:'url('+content_bg[bg_index]+')',color:content_color}">
            <div>
                <svg-icon :icon-class="svg_s.listoutline" v-if="turn_type == 1" class-name="mulu" width="25px" height="25px" @click="drawer = !drawer" /><span class="title text-3xl mt-12">{{content.name}}</span>
                <div class="name_author mt-6">
                    <svg-icon :icon-class="svg_s.bookoutline" class-name="book_name" /><span>{{content.book.name}}</span>
                    <svg-icon :icon-class="svg_s.brushoutline" class-name="book_name" /><span>{{content.book.author}}</span>
                    <svg-icon :icon-class="svg_s.languageoutline" class-name="book_name" /><span>{{content.words_number}}字</span>
                </div>
                <div class="p-8 text-lg z_content" v-html="content.content" id="contents"></div>
            </div>
            <v-expand-transition>
                <v-card v-show="menu_setting == 1" class="m-auto fixed top-0 w-full h-10 leading-10 bg-gray-800 text-white hide_class">
                    <span>{{content.name}}</span>
                </v-card>
            </v-expand-transition>
            <v-expand-transition>
                <v-card v-show="menu_setting == 1" class="m-auto fixed bottom-0 w-full h-12 bg-gray-800 text-white settings hide_class">
                    <v-btn depressed color="white" @click="get_chapter_list">目录</v-btn>
                    <v-btn depressed color="white"><router-link :to="{name:'Home'}" style="color: black">书架</router-link></v-btn>
                    <v-btn depressed color="white" @click="setting = !setting">设置</v-btn>
                </v-card>
            </v-expand-transition>
        </div>
        <div class="catalog m-auto h-12  mt-6 mb-3" v-if="turn_type == 1" :style="{background:'url('+content_bg[bg_index]+')'}">
            <span class="w-2/6 inline-block" v-if="content.prev != 0"><a @click="prev_page" class="block hover:bg-teal-500 hover:text-white transition ease-in duration-200">上一章</a></span>
            <span class="w-2/6 inline-block">
                <router-link class="block hover:bg-teal-500 cursor-pointer hover:text-white transition ease-in duration-200" :to="{name:'Chapter',params:{id:content.book.id}}">目录</router-link>
            </span>
            <span class="w-2/6 inline-block" v-if="content.next != 0"><a @click="next_page" class="block hover:bg-teal-500 hover:text-white transition ease-in duration-200">下一章</a></span>
        </div>
        <v-navigation-drawer v-model="drawer" fixed top temporary>
            <v-list nav dense>
                <v-list-item-group active-class="deep-purple--text text--accent-4">
                  <v-list-item class="c_list">
                      <router-link :to="{name:'Home'}" style="color: black">
                        <v-list-item-title>我的书架</v-list-item-title>
                      </router-link>
                  </v-list-item>
                  <v-list-item  class="c_list">
                    <v-list-item-title @click="backgroung = !backgroung">背景色</v-list-item-title>
                  </v-list-item>
                  <v-list-item  class="c_list">
                    <v-list-item-title @click="get_chapter_list">目录</v-list-item-title>
                  </v-list-item>
                    <v-list-item  class="c_list">
                    <v-list-item-title @click="read_type = !read_type">阅读模式</v-list-item-title>
                  </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>
        <v-navigation-drawer v-model="setting" fixed top temporary>
            <v-list nav dense>
                <v-list-item-group active-class="deep-purple--text text--accent-4">
                  <v-list-item  class="c_list">
                    <v-list-item-title @click="backgroung = !backgroung">背景色</v-list-item-title>
                  </v-list-item>
                  <v-list-item  class="c_list">
                    <v-list-item-title @click="read_type = !read_type">阅读模式</v-list-item-title>
                  </v-list-item>
                </v-list-item-group>
            </v-list>
        </v-navigation-drawer>
        <v-navigation-drawer v-model="read_type" fixed top temporary :style="{height:screen_heights+'px'}">
            <v-list>
                  <v-list-item link @click="change_type(1)" style="margin-top: 15px">
                    <v-list-item-title>上下滑动</v-list-item-title>
                  </v-list-item>
                  <v-list-item link @click="change_type(2)" style="margin-top: 15px">
                    <v-list-item-title>左右滑动</v-list-item-title>
                  </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <v-navigation-drawer v-model="backgroung" fixed top temporary id="bg_list" :style="{height:screen_heights+'px'}">
            <v-list v-for="(bg,index) in content_bg" v-bind:key="bg">
                  <v-list-item link @click="change_bgimg(index)" style="margin-top: 15px">
                    <v-list-item-title><img class="inline mx-2" style="width: 100%; height: 50px" :src="bg"></v-list-item-title>
                  </v-list-item>
            </v-list>
        </v-navigation-drawer>
        <v-navigation-drawer v-model="mulu" fixed top temporary>
            <v-list class="lists">
                  <v-card elevation="16" class="mx-auto">
                  <v-virtual-scroll :bench="benched" :items="chapter_list" item-height="64" :style="{height:screen_heights+'px'}">
                    <template  v-slot="{ item }">
                      <v-list-item :key="item">
                            <v-list-item-title :id="item.id == chapter_id ? 'select_chapter' : ''" @click="jump_page(item.id, $event)">{{ item.name }}</v-list-item-title>
                      </v-list-item>
                    </template>
                  </v-virtual-scroll>
                </v-card>
              </v-list>
        </v-navigation-drawer>
    </div>
</template>

<script>
    export default {
        name: "Info",
        data(){
            return {
                chapter_id:this.$route.params.id,
                bg_img:['https://s1.ax1x.com/2020/07/11/UQ1N3F.jpg','https://s1.ax1x.com/2020/07/11/UQ1Uc4.jpg'],
                big_box: {
                    background:"url('https://s1.ax1x.com/2020/07/11/UQ1N3F.jpg') fixed"
                },
                content_bg: [
                    require("../assets/images/content_bg1.png"),
                    require("../assets/images/content_bg2.png"),
                    require("../assets/images/content_bg3.png"),
                    require("../assets/images/content_bg4.png"),
                    require("../assets/images/content_bg5.png"),
                    require("../assets/images/content_bg6.png"),
                    require("../assets/images/content_bg7.png"),
                    require("../assets/images/content_bg8.png"),
                    require("../assets/images/content_bg9.png"),
                ],
                svg_s:{
                    listoutline:'list-outline',
                    bookoutline:'book-outline',
                    brushoutline:'brush-outline',
                    languageoutline:'language-outline'
                },
                bg_index:0,
                content:[],
                loading:false,
                chapter_list: [],
                page: 1,
                limit: 20,
                benched: 10,
                items: [],
                drawer: false,
                backgroung: false,
                read_type: false,
                mulu: false,
                setting: false,
                screen_heights: 0,
                content_color: "#000000", // 内容的字体颜色
                count_page: 0,  //翻页模式  总页码
                current_page: 1, //翻页模式  当前页码
                count_height:0,//页面总像素高度
                turn_type: 2, //阅读方式  1上下滑动  2左右滑动
                menu_setting: 0,//菜单
            }
        },
        created(){
            let rand = Math.floor((Math.random()*2));
            let img_url = this.bg_img[rand];
            this.big_box.background = "url(" + img_url + ") fixed";
            let bg_index = localStorage.getItem('bg_index');
            if(bg_index){
                this.bg_index = bg_index
            }else{
                localStorage.setItem('bg_index', 0);
            }
            if(bg_index == 7 || bg_index == 8){
                this.content_color = "#e8e8e8";
                this.svg_s.listoutline = 'list-outline_white';
                this.svg_s.bookoutline = 'book-outline_white';
                this.svg_s.brushoutline = 'brush-outline_white';
                this.svg_s.languageoutline = 'language-outline_white';
            }else{
                this.content_color = "#000000";
                this.svg_s.listoutline = 'list-outline';
                this.svg_s.bookoutline = 'book-outline';
                this.svg_s.brushoutline = 'brush-outline';
                this.svg_s.languageoutline = 'language-outline';
            }

        },
        mounted(){
          this.loading = true;
          this.get_content(this.$route.params.id,1);
          this.screen_heights = window.screen.height;
        },
        methods:{
            next_page(){
                this.loading = true;
                this.get_content(this.content.next);
                this.$router.push({params:{id:this.content.next}});
                this.chapter_id = this.content.next;
                if(this.turn_type === 1){
                    window.scrollTo(0,0);
                }else{
                    this.current_page = 1;
                    document.documentElement.scrollTop = 0;
                }
            },
            prev_page(){
                this.loading = true;
                this.get_content(this.content.prev);
                this.$router.push({params:{id:this.content.prev}});
                this.chapter_id = this.content.prev;
                if(this.turn_type === 1){
                    window.scrollTo(0,0);
                }else{
                    let _this = this;
                    setTimeout(function () {
                        document.documentElement.scrollTop = _this.count_height;
                        _this.current_page = _this.count_page;
                    },500);
                }
            },
            jump_page(chapter_id,event){
                this.sheet = false;
                this.loading = true;
                let el = event.currentTarget;
                el.setAttribute('id','select_chapter');
                this.$router.push({name:'Info',params:{id:chapter_id}});
                this.chapter_id = chapter_id;
                this.get_content(chapter_id);
            },
            get_content(chapter_id,first_into=0){
                this.$axios.get('/api/chapter/', {params:{id:chapter_id}}).then(res=>{
                    this.content = res.data;
                    this.loading = false;
                    document.title = this.content.name;
                    localStorage.setItem("book_continue_" + this.content.book.id, chapter_id);
                    localStorage.setItem("book_continue_title_" + this.content.book.id, this.content.name);
                    if(first_into === 1){
                        let chapter_list_cash = localStorage.getItem('chapter_list_' + res.data.book.id);
                        let ex_time = localStorage.getItem('ex_time_' + res.data.book.id);
                        let timestamp = new Date().getTime().toString().substr(0,10);
                        if(chapter_list_cash != null && ex_time + 7200 > timestamp){
                            this.chapter_list = JSON.parse(chapter_list_cash)
                        }else{
                            this.$axios.get("/api/chapter_list/", {params:{'book_id':res.data.book.id,'page':1,'limit':10000}}).then(res2=>{
                                this.chapter_list = res2.data.list;
                                localStorage.setItem('chapter_list_' + res.data.book.id, JSON.stringify(res2.data.list));
                                localStorage.setItem('ex_time_' + res.data.book.id, Number(timestamp)+7200);
                            })
                        }
                    }
                    let _this = this;
                    let read_type = localStorage.getItem('read_type');
                    if(!read_type){
                        read_type = 2
                    }
                    _this.change_type(read_type);
                    if(read_type == 2){
                        setTimeout(function () {
                            document.getElementById('contents').style.paddingBottom = 0 + "px";
                            _this.count_height = document.documentElement.scrollHeight;
                            _this.count_page = Math.ceil(_this.count_height/window.screen.height);
                            _this.pdbm = window.screen.height*_this.count_page-_this.count_height;
                            document.getElementById('contents').style.paddingBottom = _this.pdbm + "px";
                        },200)
                    }
                })
            },
            get_chapter_list(){
                this.mulu = true;
                let _this = this;
                setTimeout(function () {
                    document.getElementsByClassName('v-virtual-scroll')[0].scrollTop=(_this.content.prev_count-3)*64
                },50)
            },
            change_bgimg(key){
                this.bg_index = key;
                localStorage.removeItem('bg_index');
                localStorage.setItem('bg_index', key);
                if(key === 7 || key === 8){
                    this.content_color = "#e8e8e8";
                    this.svg_s.listoutline = 'list-outline_white';
                    this.svg_s.bookoutline = 'book-outline_white';
                    this.svg_s.brushoutline = 'brush-outline_white';
                    this.svg_s.languageoutline = 'language-outline_white';
                }else{
                    this.content_color = "#000000";
                    this.svg_s.listoutline = 'list-outline';
                    this.svg_s.bookoutline = 'book-outline';
                    this.svg_s.brushoutline = 'brush-outline';
                    this.svg_s.languageoutline = 'language-outline';
                }
            },
            touch_wz(e) {
                if(this.turn_type == 2){
                    let touch_x = e.targetTouches[0].clientX;
                    let touch_y = e.targetTouches[0].clientY;
                    let pd_width = document.documentElement.clientWidth;
                    let pd_height = document.documentElement.clientHeight;
                    let effective_lr = (pd_width - 80) / 2;
                    let effective_tb = pd_height / 2;
                    if(touch_y > effective_tb/2 && touch_y < effective_tb/2*3){
                        if (touch_x > effective_lr && touch_x < effective_lr + 80) {
                            this.menu_setting = !this.menu_setting;
                        }
                        if (touch_x < effective_lr) {
                            if(this.drawer || this.backgroung || this.mulu || this.setting){
                                return;
                            }
                            this._scroll_top(window.screen.height*(this.current_page-2),this.current_page-1);
                            this.menu_setting = 0;
                        } else if (touch_x > effective_lr + 80){
                            if(this.drawer || this.backgroung || this.mulu || this.setting){
                                return;
                            }
                            this._scroll_top(window.screen.height*(this.current_page),this.current_page+1);
                            this.menu_setting = 0;
                        }
                    }
                }
            },
            _scroll_top(top,current_page){
                if(current_page <= 0){
                    this.prev_page();
                    return;
                }
                if(current_page >= this.count_page){
                    current_page = this.count_page
                }
                if(top <= 0){
                    top = 0
                }
                if(top >= this.count_height){
                    this.next_page();
                    return;
                }
                this.current_page = current_page;
                document.documentElement.scrollTop = top;
            },
            change_type(type){
                this.turn_type = type;
                if(type == 1){
                    document.documentElement.style.setProperty("overflow","auto","important");
                    let x = document.getElementsByClassName('hide_class');
                    for (let i = 0; i < x.length; i++) {
                        x[i].style.display = "none";
                    }
                    localStorage.removeItem('read_type');
                    localStorage.setItem('read_type', type);
                }else if(type == 2){
                    document.documentElement.style.setProperty("overflow","hidden","important");
                    localStorage.removeItem('read_type');
                    localStorage.setItem('read_type', type);
                }
            }
        },
    }
</script>

<style scoped>
.title{
    display: inline-block;
}
.box{
    padding-top: 1px;
    padding-bottom: 1px;
}
.contents{
    text-align: center;
}
.catalog{
    width: 50%;
    line-height: 3rem;
    text-align: center;
}
.z_content{
    font-family: "PingFangSC Medium";
    text-align: left !important;
    padding-bottom: 0;
}
.name_author ul li{
    float: left;
}
.name_author span{
    margin: 0 30px 0 5px;
}
.mulu{
    margin-top: -7px;
    margin-right: 3px;
}
.lists{
    padding: 0.1px;
}
.book_name_list{
    position: fixed;
    width: 100%;
    background: white;
    z-index: 203;
    margin-bottom: 30px;
}
.book_name_list + div{
    margin-top: 36px;
}
#select_chapter{
    color: red;
}
.setting{
    width: 100%;
    background: white;
    height: 66px;
    text-align: center;
}
@media screen and (max-width: 1200px) {
    .contents{
        width: 100%;
        margin-top: 0px;
    }
    .box{
        padding-top: 0px;
    }
    .z_content{
        padding: 1.8rem 10px 0;
        line-height: 24px;
    }
    .title{
        font-size: 1.5rem;
    }
    .catalog{
        width: 100%;
    }
}
.c_list{
    height: 64px;
}
.c_list .v-list-item__title{
    font-size: 16px !important;
}
.bg_list{
    min-height: 600px;
    max-height: 1000px;
}
.settings button{
    display: inline-block;
    line-height: 3rem;
    width: 33%;
    height: 3rem !important;
}
</style>
<style>
.list_scroll{
    overflow-y: scroll !important;
}
</style>