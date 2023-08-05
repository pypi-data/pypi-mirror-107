'use strict';

suite('rb/newReviewRequest/views/RepositorySelectionView', function () {
    var collection = void 0;
    var view = void 0;

    beforeEach(function () {
        collection = new Backbone.Collection([{ name: 'Repo 1' }, { name: 'Repo 2' }, { name: 'Repo 3' }], {
            model: RB.Repository
        });

        view = new RB.RepositorySelectionView({
            collection: collection
        });
    });

    describe('Rendering', function () {
        it('With items', function () {
            view.render();
            var children = view.$el.find('.repository');

            expect(children.length).toBe(collection.models.length);

            for (var i = 0; i < children.length; i++) {
                var name = collection.models[i].get('name');
                expect($(children[i]).text().strip()).toBe(name);
            }
        });
    });

    describe('Selected event', function () {
        it('When clicked', function () {
            var handlerCalled = false;

            view.render();
            view.on('selected', function (repository) {
                expect(repository.get('name')).toBe('Repo 2');
                handlerCalled = true;
            });

            var children = view.$el.find('.repository');
            $(children[1]).click();

            expect(handlerCalled).toBe(true);
        });
    });
});

//# sourceMappingURL=repositorySelectionViewTests.js.map