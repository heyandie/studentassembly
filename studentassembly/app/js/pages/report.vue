<template lang="jade">
v-header
section.page__wrapper
  .content__wrapper
    .content__section
      h1 File a report
      .form__wrapper
        form
          .form__element
            .form__label School
            select
              option University of the Philippines - Diliman
              option Ateneo de Manila University
              option De La Salle University - Manila
          .form__element
            .form__label Type of Report
            select
              option Cleanliness / Environmental
              option Curriculum
              option Distance or Accesibility
              option Discrimination
              option Enrollment Process
              option Fees
              option Grades
              option Harassment
              option Maintenance
              option Policies
              option Process (Administrative)
              option Supplies
          .form__element
            .form__label Report Details
            textarea(rows="10")
          .form__element
            .form__label Attachments
            .form__note Each file has a 5MB limit.
            .form__attachments
              .form__attachment
              .form__attachment
              .form__attachment
          .form__element
            .form__label Do you want to publish your report?
            .form__note Agreeing to publish your report does not guarantee its posting. Student Assembly reserves the right to not publish reports that may be damaging / harmful to others.
            .form__radio
              input(type="radio" name="publish" value="yes")
              label Yes
            .form__radio
              input(type="radio" name="publish" value="no")
              label No
          .form__element
            .form__label Are you willing to provide your contact details?
            .form__note If this is a sexual harassment or discrimination report and you would like to pursue legal action, kindly give your contact information.
            input(type="text" placeholder="Name")
            input(type="email" placeholder="Email Address")
            input(type="text" placeholder="Mobile Number")
          .form__element
            button(type="submit")
              span Submit


</template>

<script>
var Header = require('../components/header.vue');
var Spinner = require('../components/spinner.vue');

module.exports = {
  data: function() {
    return {
      msg: 'Create an account',
    }
  },
  methods: {
  },
  components: {
    'v-header': Header,
    'v-spinner': Spinner
  }
}
</script>
