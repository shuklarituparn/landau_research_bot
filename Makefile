db:
	@echo "=== Creating DB ==="
	@bash ./bot/scripts/createdb.sh
	@echo "=== Done ==="
tools:
	@echo "=== Setting linting ==="
	@bash ./bot/scripts/setup.sh
	@echo "=== Done ==="

autoformat:
	@echo "=== Running auto formatter ==="
	@bash ./bot/scripts/formatter.sh
	@echo "=== Ran auto formatter ==="