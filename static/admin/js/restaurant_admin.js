(() => {
    function slugify(value) {
        return (value || '')
            .toLowerCase()
            .trim()
            .replace(/[^a-z0-9]+/g, '_')
            .replace(/^_+|_+$/g, '');
    }

    function initRestaurantAdminForm() {
        const subdomainInput = document.getElementById('id_subdomain');
        const dbNameInput = document.getElementById('id_db_name');
        if (!subdomainInput || !dbNameInput) return;

        // If user edits db_name manually, stop auto-overwriting it.
        dbNameInput.addEventListener('input', () => {
            dbNameInput.dataset.manual = '1';
        });

        const syncDbName = () => {
            if (dbNameInput.dataset.manual === '1') return;
            const slug = slugify(subdomainInput.value);
            if (!slug) return;
            dbNameInput.value = `tenant_${slug}_db`;
        };

        subdomainInput.addEventListener('input', syncDbName);
        subdomainInput.addEventListener('change', syncDbName);

        // Auto-fill on load if this is add form/default value.
        if (!dbNameInput.value || dbNameInput.value === 'tenant_restaurant_db') {
            syncDbName();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initRestaurantAdminForm);
    } else {
        initRestaurantAdminForm();
    }
})();
