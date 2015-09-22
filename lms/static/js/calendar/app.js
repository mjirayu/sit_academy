$(function(){
    var Event = Backbone.Model.extend({
    });

    var Events = Backbone.Collection.extend({
        model: Event,
        url: '/api/user/v1/events/'
    });

    var EventsView = Backbone.View.extend({
        initialize: function(){
            _.bindAll(this,
              'render',
              'addAll',
              'select',
              'addOne',
              'eventClick',
              'change',
              'eventDropOrResize',
              'destroy'
            );
            this.collection.bind('reset', this.addAll);
            this.collection.bind('add', this.addOne);
            this.collection.bind('change', this.change);
            this.collection.bind('destroy', this.destroy);
        },
        render: function() {
            this.$el.fullCalendar({
                header: {
                    left: 'prev,next today',
                    center: 'title',
                    right: 'month',
                    ignoreTimezone: false
                },
                selectable: true,
                selectHelper: true,
                editable: true,
                select: this.select,
                eventClick: this.eventClick,
                eventDrop: this.eventDropOrResize,
                eventResize: this.eventDropOrResize
            });
        },
        addAll: function(){
            this.$el.fullCalendar('addEventSource', this.collection.toJSON());
        },
        select: function(startDate, endDate) {
          var eventModel = new Event({start: startDate, end: endDate});
          var eventView = new EventView({
            collection: this.collection,
            model: eventModel
          });
          eventView.render();
        },
        addOne: function(event) {
          this.$el.fullCalendar('renderEvent', event.toJSON(), true);
        },
        eventClick: function(fcEvent) {
          var eventView = new EventView({
            model: this.collection.get(fcEvent.id),
          });
          this.$el.find('.fc-event-time').hide();
          eventView.render();
        },
        change: function(event) {
          var fcEvent = this.$el.fullCalendar('clientEvents', event.get('id'))[0];
          fcEvent.title = event.get('title');
          fcEvent.color = event.get('color');
          this.$el.fullCalendar('updateEvent', fcEvent);
        },
        eventDropOrResize: function(fcEvent) {
          this.collection.get(fcEvent.id).save({start: fcEvent.start, end: fcEvent.end});
        },
        destroy: function(event) {
          this.$el.fullCalendar('removeEvents', event.id);
        }
    });

    var EventView = Backbone.View.extend({
        el: $('#eventDialog'),
        initialize: function() {
            _.bindAll(this, 'render', 'close', 'open', 'save', 'destroy');
        },
        render: function() {
            var buttons = {'Ok': this.save};
            if (!this.model.isNew()) {
                _.extend(buttons, {'Delete': this.destroy});
            }
            _.extend(buttons, {'Cancel': this.close});

            this.$el.dialog({
                modal: true,
                title: (this.model.isNew() ? 'New' : 'Edit') + ' Event',
                buttons: buttons,
                open: this.open
            });

            return this;
        },
        open: function() {
            this.$('#title').val(this.model.get('title'));
            this.$('#color').val(this.model.get('color'));
        },
        close: function() {
            this.$el.dialog('close');
        },
        save: function() {
            this.model.set({
              'title': this.$('#title').val(),
              'color': this.$('#color').val()
            });
            if (this.model.isNew()) {
              this.collection.create(this.model, {success: this.close, wait: true});
            } else {
              this.model.save({}, {success: this.close});
            }
        },
        destroy: function() {
          this.model.destroy({success: this.close});
        }
    });

    var events = new Events();
    new EventsView({el: $("#calendar"), collection: events}).render();
    events.fetch();
});
