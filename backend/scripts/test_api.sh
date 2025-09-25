#!/bin/bash

# =============================================================================
# API Test Script for LLM Toolset Backend
# =============================================================================

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# =============================================================================
# Configuration
# =============================================================================

readonly BASE_URL="http://localhost:15050"
readonly HEADERS="Content-Type: application/json"
readonly MODEL_NAME="Qwen3-8B"
# Inference configuration for memory calculations
readonly INFERENCE_CONFIG=(
    "model_name=${MODEL_NAME}"
    "precision=bfloat16"
    "batch_size=1"
    "sequence_length=8192"
    "kv_cache_precision=bfloat16"
    "use_flash_attention=1"
    "use_page_attention=1"
)
# Training configuration for memory calculations
readonly TRAINING_CONFIG=(
    "model_name=${MODEL_NAME}"
    "precision=bfloat16"
    "batch_size=1"
    "sequence_length=8192"
    "optimizer=AdamW"
    "trainable_parameters=1"
    "use_flash_attention=1"
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
    payload=$(build_json_payload INFERENCE_CONFIG)
    make_request "POST" "/api/memory/inference" "$payload" "Inference Memory Calculation"
}

test_memory_training() {
    local payload
    payload=$(build_json_payload TRAINING_CONFIG)
    make_request "POST" "/api/memory/training" "$payload" "TrainingMemory Calculation"
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
