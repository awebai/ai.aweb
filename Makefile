.PHONY: help docs-sync

help:
	@echo "Targets:"
	@echo "  docs-sync   Refresh support docs from ../ac/docs/support/"

# Source of truth lives in ac. Amy reads the copy here because she
# must not be given read access to the rest of ac.
AC_SUPPORT := ../ac/docs/support
LOCAL_SUPPORT := docs/support

docs-sync:
	@test -d $(AC_SUPPORT) || { echo "missing $(AC_SUPPORT); is ac checked out as a sibling?"; exit 1; }
	@mkdir -p $(LOCAL_SUPPORT)
	@cp $(AC_SUPPORT)/*.md $(LOCAL_SUPPORT)/
	@echo "synced $(AC_SUPPORT)/*.md -> $(LOCAL_SUPPORT)/"
	@python3 scripts/splice-recovery-into-runbook.py
