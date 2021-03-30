import Vue from 'vue';
import Vuetify, {VProgressLinear} from 'vuetify/lib';
Vue.use(Vuetify, {
  components: { VProgressLinear },
});

export default new Vuetify({
    theme: {
        isDark: true,
    },
});
