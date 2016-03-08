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
            .form__select
              select(name="school")
                option(disabled selected hidden) Choose a school...
                option(v-for="school in schools" value="{{ school.id }}") {{ school.name }}
          .form__element
            .form__label Type of Report
            .form__select
              select(name="category")
                option(disabled selected hidden) Choose a category..
                option(v-for="category in categories" value="{{ category.id }}") {{ category.name }}
          .form__element
            .form__label Report Details
            textarea(rows="10" name="text" placeholder="State the corruption case in detail.")
          .form__element
            .form__label Attachments
            .form__note It can be a document or an image. Each file has a 3MB limit.
            .form__attachments
              .form__attachment
                input(type="file" id="file1" name="files[]")
                label(for="file1")
              .form__attachment
                input(type="file" id="file2" name="files[]")
                label(for="file2")
              .form__attachment
                input(type="file" id="file3" name="files[]")
                label(for="file3")
          .form__element
            .form__label Do you want to publish your report?
            .form__note Agreeing to publish your report does not guarantee its posting. Student Assembly reserves the right to not publish reports that may be damaging / harmful to others.
            .form__radio
              input(type="radio" name="allow_publish" id="allow_publish_1" value="yes")
              label(for="allow_publish_1") Yes, publish my report.
            .form__radio
              input(type="radio" name="allow_publish" id="allow_publish_2" value="no" checked)
              label(for="allow_publish_2") No, don't publish my report.
          .form__element
            .form__label Are you willing to provide your contact details?
            .form__note If this is a sexual harassment or discrimination report and you would like to pursue legal action, kindly give your contact information.
            .form__radio
              input(type="radio" name="allow_contact" id="allow_contact_1" value="yes" @click="allowContact = true")
              label(for="allow_contact_1") Yes, I would to give my contact.
            .form__radio
              input(type="radio" name="allow_contact" id="allow_contact_2" value="no" @click="allowContact = false" checked)
              label(for="allow_contact_2") No, I don't want to give my contact.
            template(v-if="allowContact")
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
      allowContact: false,
      schools: null,
      categories: null
    }
  },
  methods: {
  },
  ready: function() {
    var that = this;
    client({ path: 'schools' }).then(
      function (response) {
        that.schools = response.entity;
      },
      function (response) {
        console.log('Error trying to fetch schools. Contact the server again.');
      }
    );
    client({ path: 'categories' }).then(
      function (response) {
        that.categories = response.entity;
      },
      function (response) {
        console.log('Error trying to fetch categories. Contact the server again.');
      }
    );
  },
  components: {
    'v-header': Header,
    'v-spinner': Spinner
  }
}
</script>
