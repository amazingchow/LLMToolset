#!/bin/bash

# =============================================================================
# API Test Script for LLM Toolset Backend
# =============================================================================
# This script tests various API endpoints of the LLM Toolset backend service.
# It performs health checks, model queries, and memory calculations.

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# =============================================================================
# Configuration
# =============================================================================

readonly BASE_URL="http://localhost:15050"
readonly MODEL_NAME="Qwen3-8B-Base"
readonly HEADERS="Content-Type: application/json"

# Model configuration for memory calculations
readonly MODEL_CONFIG=(
    "model_name=${MODEL_NAME}"
    "precision=float16"
    "batch_size=1"
    "sequence_length=2048"
    "hidden_size=4096"
    "num_hidden_layers=36"
    "num_attention_heads=32"
)

# Training-specific configuration
readonly TRAINING_CONFIG=(
    "optimizer=AdamW"
    "trainable_parameters=100"
)

# =============================================================================
# Helper Functions
# =============================================================================

# Print colored output for better readability
print_header() {
    echo -e "\n\033[1;34m=== $1 ===\033[0m"
}

print_success() {
    echo -e "\033[1;32m✓ $1\033[0m"
}

print_error() {
    echo -e "\033[1;31m✗ $1\033[0m" >&2
}

# Make HTTP request with error handling
make_request() {
    local method="$1"
    local endpoint="$2"
    local data="${3:-}"
    local description="$4"
    
    print_header "$description"
    
    if [[ -n "$data" ]]; then
        # POST request with JSON data
        if ! curl -s -X "$method" \
                -H "$HEADERS" \
                -d "$data" \
                "$BASE_URL$endpoint" | jq .; then
            print_error "Failed to $description"
            return 1
        fi
    else
        # GET request
        if ! curl -s "$BASE_URL$endpoint" | jq .; then
            print_error "Failed to $description"
            return 1
        fi
    fi
    
    print_success "$description completed"
}

# Build JSON payload from key-value pairs
build_json_payload() {
    local config_array_name="$1"
    local json="{"
    local first=true
    
    # Use eval to access the array by name (compatible with older Bash)
    eval "local array_length=\${#$config_array_name[@]}"
    
    for ((i=0; i<array_length; i++)); do
        eval "local item=\${$config_array_name[$i]}"
        
        if [[ "$first" == true ]]; then
            first=false
        else
            json+=","
        fi
        
        local key="${item%%=*}"
        local value="${item#*=}"
        
        # Handle numeric values (don't quote them)
        if [[ "$value" =~ ^[0-9]+(\.[0-9]+)?$ ]]; then
            json+="\"$key\": $value"
        else
            json+="\"$key\": \"$value\""
        fi
    done
    
    json+="}"
    echo "$json"
}

# =============================================================================
# Main Test Functions
# =============================================================================

test_health_check() {
    make_request "GET" "/health" "" "Health Check"
}

test_models_list() {
    make_request "GET" "/api/models" "" "List Available Models"
}

test_model_details() {
    make_request "GET" "/api/models/$MODEL_NAME" "" "Get Model Details"
}

test_config_options() {
    make_request "GET" "/api/config/options" "" "Get Configuration Options"
}

test_memory_inference() {
    local payload
    payload=$(build_json_payload MODEL_CONFIG)
    make_request "POST" "/api/memory/inference" "$payload" "Memory Inference Calculation"
}

test_memory_training() {
    local payload
    # Combine model config with training config
    local combined_config=("${MODEL_CONFIG[@]}" "${TRAINING_CONFIG[@]}")
    payload=$(build_json_payload combined_config)
    make_request "POST" "/api/memory/training" "$payload" "Memory Training Calculation"
}

# =============================================================================
# Main Execution
# =============================================================================

main() {
    echo "🚀 Starting LLM Toolset API Tests"
    echo "📍 Base URL: $BASE_URL"
    echo "🤖 Test Model: $MODEL_NAME"
    echo ""
    
    # Run all tests
    test_health_check
    test_models_list
    test_model_details
    test_config_options
    test_memory_inference
    test_memory_training
    
    echo ""
    print_success "All API tests completed successfully! 🎉"
}

# Run main function if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi
