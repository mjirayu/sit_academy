var Note = Backbone.Model.extend({
  idAttribute: 'id',
});

var Notes = Backbone.Collection.extend({
    model: Note,
    url: '/api/user/v1/reminders/'
});

var NoteView = Backbone.View.extend({
  template: _.template($("#note-template").html()),
  tagName: 'div',
  className: 'reminder-note',
  events: {
    'click .save': 'save',
    'click .remove': 'removeModel'
  },
  render: function() {
    this.el.innerHTML = this.template(this.model.toJSON());
    return this;
  },
  removeModel: function() {
    this.model.destroy();
  },
  save: function(event) {
    this.model.set({'text': this.$('#text-area').val()})
    this.model.save();
  },
});

var NotesView = Backbone.View.extend({
  initialize: function() {
    this.listenTo(this.collection, 'add', this.addNote);
    this.listenTo(this.collection, 'remove', this.removeNote);
  },
  events: {
    'click #add-note': 'createNote'
  },
  template: _.template($("#notes-template").html()),
  render: function() {
    this.el.innerHTML = this.template(this.collection);
    this.collection.each(this.addNote.bind(this));
    return this;
  },
  addNote: function(model) {
    model.view = new NoteView({model: model});
    if($('.reminder-note').length < 3) {
      this.$('#notes').append(model.view.render().el);
    }
  },
  removeNote: function(model) {
    model.view.remove();
  },
  createNote: function(model) {
    if($('.reminder-notes').length < 3) {
      this.collection.create({
        'text': '',
      });
    }
  }
})

var notes = new Notes();
var notesView = new NotesView({collection: notes});
$('.reminder').append(notesView.render().el);
notes.fetch();
