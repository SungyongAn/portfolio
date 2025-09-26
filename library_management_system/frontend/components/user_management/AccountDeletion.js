const AccountDeletion = {
    emits: ['back-to-management'],
    data() {
        return {
            searchResults: []
        };
    },
    methods: {
        handleSearchCompleted(results) {
            this.searchResults = results;
        },
        handleDeleteCompleted(updatedResults) {
            this.searchResults = updatedResults;
        }
    },
    template: `
        <div>
            <search-accounts @search-completed="handleSearchCompleted"></search-accounts>
            <user-delete v-if="searchResults.length > 0" 
                :search-results="searchResults" 
                @delete-completed="handleDeleteCompleted">
            </user-delete>
        </div>
    `
};
