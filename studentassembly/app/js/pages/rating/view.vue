<template lang="jade">
section.page__wrapper.page--min-height
  .content__wrapper
    .content__section
      article.content__main
        .form__wrapper(v-if="$loadingRouteData")
          .spinner__wrapper
            v-spinner
            h4 Loading staff member...
        template(v-if="!$loadingRouteData")
          .form__wrapper
            .button__group.pull-right
              .button.button--tiny.button--simple#share_menu(@click="showShareMenu = !showShareMenu")
                | •••
                .dropdown__menu(v-bind:class="showShareMenu ? 'dropdown__menu--open' : ''")
                  .dropdown__menu-header
                    span Share
                  a.dropdown__menu-item(target="_blank" href="#0")
                    img.button__icon(src="/static/img/fb-logo.png" height="15")
                    span Facebook
                  a.dropdown__menu-item(target="_blank" href="https://twitter.com/intent/tweet?text=Share%20Report")
                    img.button__icon(src="/static/img/twitter-logo.png" height="14")
                    span Twitter
            h2.u-mg-b-24
              span {{ member.name }}
              br
              span.header--light {{ member.school }}
            h4.u-mg-b-12 Average of {{ member.votes }} {{ member.votes | pluralize 'rating' }}
            ul.stats
              li.stat(v-for="val in member.rating")
                p.stat__header {{ toTitleCase($key, "_") }}
                span.stat__value {{ val }} / 5

          .form__wrapper
            template(v-if="member.user_rating")
              h3.u-mg-b-24 Your rating
              ul.stats.u-mg-b-24
                li.stat.stat--small(v-for="val in member.user_rating.values")
                  p.stat__header {{ toTitleCase($key, "_") }}
                  span.stat__value {{ val }} / 5
              template(v-if="member.user_rating.comment")
                p(v-for="paragraph in splitText(member.user_rating.comment)") {{ paragraph }}
              a.button.button--tiny(@click.prevent="showRatingModal = true") Edit rating
            template(v-if="!member.user_rating")
              .u-ta-c
                p You have not rated {{ member.name }}.
                a.button.button--small(@click.prevent="showRatingModal = true") Add rating

          template(v-if="member.ratings.length")
            .form__wrapper(v-for="otherRating in member.ratings")
              h4.u-mg-b-24
                v-avatar(:alias="otherRating.alias", :inline="true", height="28px", width="28px")
                span.u-mg-l-4 {{ otherRating.alias }}'s rating
              ul.stats.u-mg-b-24
                li.stat.stat--small(v-for="(key, val) in otherRating.values")
                  p.stat__header {{ toTitleCase(key, "_") }}
                  span.stat__value {{ val }} / 5
              template(v-if="otherRating.comment")
                p(v-for="paragraph in splitText(otherRating.comment)") {{ paragraph }}

      aside.content__secondary.content--additional-info
        h4 Related staff members
        .u-mg-t-24(v-for="relatedMember in relatedMembers", v-if="relatedMember.id !== member.id")
          a(v-link="{ name: 'rate-view', params: { 'id': relatedMember.id } }")
            h5 {{ relatedMember.name }}
            p.small
              span {{ relatedMember.school | truncate }}
              br
              strong {{ relatedMember.votes || 'No' }} {{ relatedMember.votes | pluralize 'rating' }}
              span(v-if="relatedMember.votes") &nbsp;&mdash; overall: {{ relatedMember.rating.overall }}

v-modal(:show.sync="showRatingModal")
  div(slot="content", style="width:300px;")
    i.modal-close.icon.ion-android-close(@click="showRatingModal = false")
    template(v-if="!$loadingRouteData")
      form(@submit.prevent="submitRating")
        .form__element(v-for="(key, val) in member.rating")
          .form__label.u-mg-b-4 {{ toTitleCase(key, "_") }}
          .form__radio.u-mg-b-0
            .u-cf
              .pull-left
                input(
                  v-for="i in 5",
                  type="radio",
                  name="{{ key }}_{{ i + 1 }}",
                  data-tooltip="Give {{ i + 1 }} points",
                  value="{{ i + 1 }}",
                  :checked="checkRating(key, i + 1)",
                  @click="updateRating(key, $event)"
                )
              .pull-right
                small.light {{ rating.values[key] }} / 5
        .form__element
          .form__label Comment
          textarea(
            rows="2",
            name="text",
            placeholder="Write additional comments about {{ member.name }}.",
            v-model="rating.comment"
          )
        .form__element
          button(type="submit") Submit rating

</template>

<script>
import Modal from '../../components/modal.vue'
import Avatar from '../../components/avatar.vue'
import Spinner from '../../components/spinner.vue'
import { toTitleCase } from '../../util'

export default {
  route: {
    data (transition) {
      return this.$http.get('staff/' + this.$route.params.id).then(
        (response) => ({ member: response.data }),
        (response) => {
          console.log('Failed to retrieve staff member.')
        }
      )
    }
  },
  data () {
    return {
      member: null,
      relatedMembers: [],
      showRatingModal: false,
      showShareMenu: false,
      rating: {
        staff_id: null,
        values: {
          accessibility: 0,
          attendance: 0,
          communication_skills: 0,
          efficiency: 0,
          fairness: 0,
          overall: 0
        },
        comment: ''
      }
    }
  },
  filters: {
    truncate (string) {
      if (string.length > 36)
        return string.substring(0, 36) + '...'
      else
        return string
    }
  },
  watch: {
    'member': function (val) {
      if (val.user_rating)
        this.prefillRating()
      this.getOtherStaffMembers()
    }
  },
  methods: {
    toTitleCase: toTitleCase,
    splitText (text) {
      return text.split('\n\n')
    },
    checkRating (key, val) {
      return val <= this.rating.values[key]
    },
    updateRating (key, e) {
      this.rating.values[key] = parseInt(e.target.value)
    },
    prefillRating () {
      Object.keys(this.rating).forEach((key) => {
        this.rating[key] = this.member.user_rating[key]
      })
    },
    submitRating () {
      let method = this.member.user_rating ? 'put' : 'post',
          query = this.member.user_rating ? '/' + this.member.user_rating.id : ''

      this.$http('rating' + query, { method: method, data: { rating: this.rating }}).then(
        (response) => {
          this.member.user_rating = response.data
          this.showRatingModal = false
        },
        (response) => {
          console.log('Error', response)
        }
      )
    },
    getOtherStaffMembers () {
      this.$http.get('staff?school=' + this.member.school_id + '&limit=5').then(
        (response) => {
          this.relatedMembers = response.data
        },
        (response) => {
          console.log('Failed')
        }
      )
    }
  },
  ready () {
    document.addEventListener("keydown", (e) => {
      if (this.showShareMenu && e.keyCode == 27)
        this.showShareMenu = false
    })
    document.addEventListener("click", (e) => {
      if (e.target.id !== 'share_menu')
        this.showShareMenu = false
    })
  },
  components: {
    'v-modal': Modal,
    'v-avatar': Avatar,
    'v-spinner': Spinner
  }
}
</script>
