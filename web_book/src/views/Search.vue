<template>
    <div>
        <div class="m-auto max-w-screen-xl">
            <v-col sm="6" class="m-auto search_box">
                <v-text-field label="搜索书籍" sm="6" outlined class="search_input inline-block" @keyup.enter="search_book_or_author" v-model="key_word"></v-text-field>
<!--                <v-btn small color="primary" outlined class="inline-block search_button" @click="search_book_or_author">搜索</v-btn>-->
            </v-col>
            <div style="margin-top: -30px">
                <v-list flat>
                  <v-list-item-group v-model="item" color="primary">
                    <v-list-item
                      v-for="(item, i) in book_list"
                      :key="i"
                    >
                      <v-list-item-icon>
                          <router-link :to="{name:'Chapter',params:{id:item.id}}">
                        <img :src="server_domain+item.cover" alt="" width="60px">
                           </router-link>
                      </v-list-item-icon>
                      <v-list-item-content>
                      <router-link :to="{name:'Chapter',params:{id:item.id}}">
                        <v-list-item-title v-text="item.name"></v-list-item-title>
                      </router-link>
                        <v-list-item-title v-text="item.author"></v-list-item-title>
                        <v-list-item-title v-text="item.newest_chapter"></v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
<!--                <li v-for="item in book_list" v-bind:key="item"><span>{{item.name}}</span><span>{{item.author}}</span></li>-->
            </div>
        </div>
<!--        <a href="#" @click="qqLogin"><img :src="qq_logo" alt=""></a>-->
    </div>
</template>

<script>
    export default {
        name: "Search",
        data(){
            return {
                // qq_logo: require("../assets/images/qq_logo.png"),
                server_domain:'',
                key_word:'',
                book_list:[]
            }
        },
        mounted(){
            this.server_domain = this.$axios.defaults.baseURL
        },
        methods:{
            // qqLogin(){
            //     alert("功能暂无")
            // },
            search_book_or_author(){
                this.$axios.get("/api/search_book/", {params:{'key':this.key_word}}).then(res=>{
                    this.book_list = res.data.list
                })
            }
        }
    }
</script>

<style scoped>
.search_box{
    text-align: center;
}
.search_button{
    height: 56px !important;
    border-left: none;
    margin-top: -1px;
}
.search_input{
    width: 100%;
}
</style>