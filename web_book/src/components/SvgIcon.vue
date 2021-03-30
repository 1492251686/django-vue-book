<template>
  <svg :class="svgCls" :width="width" :height="height" v-on="$listeners">
    <use :xlink:href="iconName" />
  </svg>
</template>

<script>
export default {
  name: 'SvgIcon',
  props: {
    iconClass: {
      type: String,
      require: true
    },
    className: {
      type: String,
      default: ''
    },
    width: {
      type: String,
      default: '20px'
    },
    height: {
      type: String,
      default: '20px'
    }
  },
  computed: {
    iconName () {
      return `#icon-${this.iconClass}`
    },
    svgCls () {
      if (this.className) {
        return 'svg-icon inline-block fill-current ' + this.className
      } else {
        return 'svg-icon'
      }
    }
  }
}
</script>

<style lang="scss" scoped>
</style>
