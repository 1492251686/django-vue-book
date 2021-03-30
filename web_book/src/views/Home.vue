<template>
  <div class="home container">
      <div class="h-12 text-center shadow" style="line-height: 3rem">
          <router-link :to="{name:'Search'}">
        <svg-icon icon-class="search-outline" class-name="search_svg" />
          </router-link>
        <span style="margin-left: 30px">我的书架</span>
      </div>
      <div class="shelf_list">
                <v-list flat>
                  <v-list-item-group color="primary">
                    <v-list-item
                      v-for="(item, i) in book_shelf"
                      :key="i"
                      class="one_list"
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
                      <router-link :to="{name:'Info',params:{id:get_continue_id(item.id)}}" class="continue_url">
                        <span style="color: black">续读：</span>
                        <v-list-item-title v-text="get_continue_title(item.id)" class="continue_title"></v-list-item-title>
                      </router-link>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
<!--                <li v-for="item in book_list" v-bind:key="item"><span>{{item.name}}</span><span>{{item.author}}</span></li>-->
            </div>
  </div>
</template>

<script>
// @ is an alias to /src
// import HelloWorld from '@/components/HelloWorld.vue'

export default {
    name: 'Home',
    data(){
            return {
                server_domain:'',
                book_shelf:[]
            }
        },
    mounted(){
        this.server_domain = this.$axios.defaults.baseURL
        let bookshelf = localStorage.getItem("bookshelf");
        if(bookshelf){
            this.book_shelf = JSON.parse(bookshelf)
        }
    },
    methods:{
        get_continue_title(chapter_id){
            let bookshelf = localStorage.getItem("book_continue_title_" + chapter_id);
            if(bookshelf){
                return bookshelf;
            }else{
                return "暂无";
            }
        },
        get_continue_id(chapter_id){
            let bookshelf = localStorage.getItem("book_continue_" + chapter_id);
            if(bookshelf){
                return bookshelf;
            }else{
                return "暂无";
            }
        },
    }
}
</script>
<style scoped>
*{
  margin: 0;
  padding: 0;
}
.continue_title{
    display: inline;
}
.shelf_list{
    margin: 20px;
}
.one_list{
    margin-bottom: 20px;
}
.search_svg{
    float: right;
    margin: 15px;
}
.continue_url{
    overflow: hidden; /*超出隐藏*/
    text-overflow: ellipsis;/*文字隐藏后添加省略号*/
    white-space: nowrap;/*强制不换行*/
}
</style>