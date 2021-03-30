<template>
<div class="xl:pl-32">
    <v-progress-linear fixed top indeterminate color="light-blue" v-if="loading"></v-progress-linear>
    <div class="book_info m-auto mt-12 xl:pl-6 sm:text-left text_c">
        <img :src="this.$axios.defaults.baseURL+book_info.cover" class="lg:w-3/12 xl:w-2/12 shadow-xl inline-block lg:float-left mb-4"  v-if="is_called">
        <div class="text_info block sm:inline-block align-top lg:ml-5 xl:ml-8 ">
            <span class="font-black text-3xl block sm:inline text-center mr-3">{{book_info.name}}</span>
            <span class="block sm:inline text-center mb-1">{{book_info.author}}<span class="ml-6 hidden sm:inline"  v-if="is_called">著</span></span>
            <div class="xl:mt-6 hidden sm:block">{{book_info.introduction}}</div>
        </div>
        <div class="inline-block continue">
            <v-btn class="ma-2" tile color="indigo lighten-2" dark @click="join_bookshelf">{{bookshelf}}</v-btn>
            <v-btn class="ma-2" tile color="indigo lighten-2" dark @click="continue_read">{{continue_btn}}</v-btn>
        </div>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 chapter_list m-auto pt-3 clear-left sm:mt-16 mt-6">
        <div class="my-3 divide-current" v-for="item in chapter_list" v-bind:key="item.id"><router-link :to="{name:'Info',params:{id:item.id}}">{{item.name}}</router-link>
            <hr class="text-gray-500 mt-4"/></div>
    </div>
    <div class="text-center" v-if="is_called">
        <v-container class="max-width">
            <v-pagination v-model="page" class="my-4" :length="page_lenth" :total-visible="totalVisible" @input="changeData"
            ></v-pagination>
          </v-container>
    </div>
</div>
</template>

<script>
    export default {
        name: "Chapter",
        data(){
            return{
                book_id:this.$route.params.id,
                chapter_list:[],
                book_info:[],
                page:1,
                limit:20,
                totalVisible:6,
                page_lenth:0,
                is_called: false,
                loading:true,
                continue_btn:"立即阅读",
                book_continue: 0,
                bookshelf:"加入书架"
            }
        },
        created(){
           let book_continue = localStorage.getItem("book_continue_" + this.book_id);
           if(book_continue){
               this.book_continue = book_continue;
               this.continue_btn = "继续阅读"
           }
           let bookshelf_id = localStorage.getItem("bookshelf_id");
           if(bookshelf_id){
                if(JSON.parse(bookshelf_id).indexOf(this.book_id) !== -1){
                    this.bookshelf = "已在书架"
                }
           }
        },
        mounted(){
            if(window.outerWidth > 1024){
                this.limit = 99
            }
            this.get_chapter_list(this.book_id,this.page,this.limit)
        },
        methods:{
            get_chapter_list(book_id,page,limit){
                this.$axios.get("/api/chapter_list/", {params:{'book_id':book_id,'page':page,'limit':limit}}).then(res=>{
                    this.chapter_list = res.data.list;
                    this.book_info = res.data.book_info;
                    document.title = this.book_info.name + "-" + this.book_info.author;
                    this.page_lenth = Math.ceil(res.data.count/this.limit);
                    this.is_called = true;
                    this.loading = false;
                })
            },
            changeData(){
                this.get_chapter_list(this.book_id,this.page,this.limit)
            },
            continue_read(){
                if(this.book_continue !== 0){
                    this.$router.push({name: 'Info',params:{id:this.book_continue}});
                }else{
                    this.$router.push({name: 'Info',params:{id:this.chapter_list[0]['id']}});
                }
            },
            join_bookshelf() {
                if (this.bookshelf === "已在书架") {
                    console.log("已在书架！");
                    return;
                }
                let bookshelf = localStorage.getItem("bookshelf");
                let book = {
                        'id':this.book_info.id,
                        'cover':this.book_info.cover,
                        'name':this.book_info.name,
                        'author':this.book_info.author,
                    };
                if (bookshelf) {
                    let shelf = JSON.parse(bookshelf);
                    shelf.push(book);
                    localStorage.setItem("bookshelf", JSON.stringify(shelf));
                    let bookshelf_id = JSON.parse(localStorage.getItem("bookshelf_id"));
                    bookshelf_id.push(this.book_id);
                    localStorage.setItem("bookshelf_id", JSON.stringify(bookshelf_id));
                } else {
                    localStorage.setItem("bookshelf", JSON.stringify([book]));
                    localStorage.setItem("bookshelf_id", JSON.stringify([this.book_id]));
                }
                this.bookshelf = "已在书架"
            }
        }
    }
</script>

<style scoped>
.chapter_list{
    width: 70%;
    text-align: left;
}
.chapter_list a{
    color: black;
}
.book_info{
    width: 55%;
}
.text_info,.continue{
    max-width: 100%;
}
.text_info div{
    max-width: 100%;
}
@media (min-width: 640px){
    .text_info{
        max-width: 60%;
    }
    .continue{
        max-width: 80%;
        margin-top: 3rem;
        margin-left: 3rem;
    }
}
@media (max-width: 640px) {
    .text_c{
        text-align: center;
    }
    .continue{
        margin: auto;
    }
}
</style>