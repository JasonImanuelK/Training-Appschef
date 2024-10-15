/** @odoo-module */
import { registry } from "@web/core/registry";
import { download } from "@web/core/network/download";
import { BlockUI, unblockUI } from "@web/core/ui/block_ui";
import { session } from "@web/session";

registry.category("ir.actions.report handlers").add("xlsx", async (action) => {
    if (action.report_type === 'xlsx') {
        BlockUI;
        try {
            await download({
                url: '/xlsx_reports',
                data: action.data,
            });
            console.log("File download successful!");
        } catch (error) {
            this.call('crash_manager', 'rpc_error', error);
        } finally {
            unblockUI;
        }
    }
});