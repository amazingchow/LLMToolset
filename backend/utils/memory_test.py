import unittest

from utils.memory import (
    _get_activation_memory,
    _get_gradient_memory,
    _get_kv_cache,
    _get_memory,
    _get_model_weights,
    _get_optimizer_memory,
    calculate_inference_memory,
    calculate_training_memory,
)


class TestMemoryCalculations(unittest.TestCase):
    """Test cases for memory calculation functions."""

    def test_calculate_inference_memory_basic(self):
        """Test basic inference memory calculation with typical parameters."""
        result = calculate_inference_memory(
            model_size=7,  # 7B model
            precision="float16",  # 2 bytes per parameter
            batch_size=1,
            sequence_length=2048,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
        )

        # Check that all expected keys are present
        expected_keys = ["model_weights", "kv_cache", "activation_memory", "inference_memory"]
        for key in expected_keys:
            self.assertIn(key, result)
            self.assertIsInstance(result[key], str)

        # Model weights should be 7B * 2 bytes = 14GB
        self.assertIn("GB", result["model_weights"])

        # Total inference memory should include all components
        self.assertIn("GB", result["inference_memory"])

    def test_calculate_inference_memory_different_precisions(self):
        """Test inference memory calculation with different precision types."""
        base_params = {
            "model_size": 7,
            "batch_size": 1,
            "sequence_length": 2048,
            "hidden_size": 4096,
            "num_hidden_layers": 32,
            "num_attention_heads": 32,
        }

        # Test with float32 (4 bytes)
        result_fp32 = calculate_inference_memory(precision="float32", **base_params)

        # Test with float16 (2 bytes)
        result_fp16 = calculate_inference_memory(precision="float16", **base_params)

        # Test with int8 (1 byte)
        result_int8 = calculate_inference_memory(precision="int8", **base_params)

        # All should have the same structure but different memory sizes
        for result in [result_fp32, result_fp16, result_int8]:
            self.assertIn("model_weights", result)
            self.assertIn("inference_memory", result)

    def test_calculate_inference_memory_large_batch(self):
        """Test inference memory calculation with large batch size."""
        result = calculate_inference_memory(
            model_size=1,  # 1B model for easier calculation
            precision="float16",
            batch_size=32,  # Large batch
            sequence_length=1024,
            hidden_size=2048,
            num_hidden_layers=24,
            num_attention_heads=16,
        )

        # With larger batch size, KV cache and activation memory should be significant
        self.assertIn("GB", result["kv_cache"])
        self.assertIn("inference_memory", result)

    def test_calculate_training_memory_basic(self):
        """Test basic training memory calculation with typical parameters."""
        result = calculate_training_memory(
            model_size=7,  # 7B model
            precision="float16",
            batch_size=1,
            sequence_length=2048,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
            optimizer="AdamW",
            trainable_parameters=100,  # 100% of parameters are trainable
        )

        # Check that all expected keys are present
        expected_keys = [
            "model_weights",
            "kv_cache",
            "activation_memory",
            "optimizer_memory",
            "gradients_memory",
            "training_memory",
        ]
        for key in expected_keys:
            self.assertIn(key, result)
            self.assertIsInstance(result[key], str)

        # Training memory should be significantly larger than inference
        self.assertIn("GB", result["training_memory"])

    def test_calculate_training_memory_different_optimizers(self):
        """Test training memory calculation with different optimizers."""
        base_params = {
            "model_size": 7,
            "precision": "float16",
            "batch_size": 1,
            "sequence_length": 2048,
            "hidden_size": 4096,
            "num_hidden_layers": 32,
            "num_attention_heads": 32,
            "trainable_parameters": 100,
        }

        # Test with AdamW (8x multiplier)
        result_adamw = calculate_training_memory(optimizer="AdamW", **base_params)

        # Test with SGD (4x multiplier)
        result_sgd = calculate_training_memory(optimizer="SGD", **base_params)

        # Test with Quantized AdamW (2x multiplier)
        result_qadamw = calculate_training_memory(optimizer="Quantized AdamW", **base_params)

        # All should have optimizer memory, but different amounts
        for result in [result_adamw, result_sgd, result_qadamw]:
            self.assertIn("optimizer_memory", result)
            self.assertIn("training_memory", result)

    def test_calculate_training_memory_partial_trainable(self):
        """Test training memory calculation with partial trainable parameters."""
        result = calculate_training_memory(
            model_size=7,
            precision="float16",
            batch_size=1,
            sequence_length=2048,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
            optimizer="AdamW",
            trainable_parameters=10,  # Only 10% of parameters are trainable
        )

        # Should still have all components but optimizer and gradient memory should be reduced
        expected_keys = [
            "model_weights",
            "kv_cache",
            "activation_memory",
            "optimizer_memory",
            "gradients_memory",
            "training_memory",
        ]
        for key in expected_keys:
            self.assertIn(key, result)

    def test_calculate_memory_zero_values(self):
        """Test memory calculation with zero values."""
        # Test inference with zero model size
        result_inf = calculate_inference_memory(
            model_size=0,
            precision="float16",
            batch_size=1,
            sequence_length=2048,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
        )

        # Should handle zero gracefully
        self.assertIn("model_weights", result_inf)

        # Test training with zero batch size
        result_train = calculate_training_memory(
            model_size=7,
            precision="float16",
            batch_size=0,
            sequence_length=2048,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
            optimizer="AdamW",
            trainable_parameters=100,
        )

        self.assertIn("training_memory", result_train)

    def test_calculate_memory_invalid_precision(self):
        """Test memory calculation with invalid precision."""
        result = calculate_inference_memory(
            model_size=7,
            precision="invalid_precision",  # Invalid precision
            batch_size=1,
            sequence_length=2048,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
        )

        # Should handle invalid precision gracefully (return empty or warning)
        self.assertIn("model_weights", result)

    def test_calculate_memory_invalid_optimizer(self):
        """Test training memory calculation with invalid optimizer."""
        result = calculate_training_memory(
            model_size=7,
            precision="float16",
            batch_size=1,
            sequence_length=2048,
            hidden_size=4096,
            num_hidden_layers=32,
            num_attention_heads=32,
            optimizer="InvalidOptimizer",  # Invalid optimizer
            trainable_parameters=100,
        )

        # Should handle invalid optimizer gracefully
        self.assertIn("optimizer_memory", result)
        self.assertIn("training_memory", result)

    def test_helper_function_get_memory(self):
        """Test the _get_memory helper function."""
        # Test with bytes
        result = _get_memory([512])
        self.assertEqual(result, "512 Bytes")

        # Test with KB
        result = _get_memory([2048])
        self.assertEqual(result, "2.00 KB")

        # Test with MB
        result = _get_memory([2097152])  # 2MB
        self.assertEqual(result, "2.00 MB")

        # Test with GB
        result = _get_memory([2147483648])  # 2GB
        self.assertEqual(result, "2.00 GB")

        # Test with TB
        result = _get_memory([2199023255552])  # 2TB
        self.assertEqual(result, "2.00 TB")

        # Test with zero (shows warning because 0 is not > 0)
        result = _get_memory([0])
        self.assertEqual(result, " * ")

        # Test with negative values (should show warning)
        result = _get_memory([1000, -500])
        self.assertIn("*", result)  # Warning indicator

        # Test with multiple values
        result = _get_memory([1024, 1024])
        self.assertEqual(result, "2.00 KB")

    def test_helper_function_get_model_weights(self):
        """Test the _get_model_weights helper function."""
        # Test with valid inputs
        result = _get_model_weights(7, "float16")  # 7B model, float16
        expected = 7 * 2 * (10**9)  # 7B parameters * 2 bytes * 10^9
        self.assertEqual(result, expected)

        # Test with invalid precision
        result = _get_model_weights(7, "invalid")
        self.assertEqual(result, 0)

        # Test with zero model size
        result = _get_model_weights(0, "float16")
        self.assertEqual(result, 0)

    def test_helper_function_get_kv_cache(self):
        """Test the _get_kv_cache helper function."""
        # Test with valid inputs
        result = _get_kv_cache("float16", 1, 2048, 4096, 32)
        expected = 2 * 1 * 2048 * 32 * 4096 * 2  # 2 * batch * seq * layers * hidden * bytes
        self.assertEqual(result, expected)

        # Test with invalid precision
        result = _get_kv_cache("invalid", 1, 2048, 4096, 32)
        self.assertEqual(result, 0)

    def test_helper_function_get_activation_memory(self):
        """Test the _get_activation_memory helper function."""
        # Test with valid inputs
        result = _get_activation_memory(1, 2048, 4096, 32)
        self.assertIsInstance(result, (int, float))  # Can return float due to division
        self.assertGreater(result, 0)

        # Test with zero values
        result = _get_activation_memory(0, 2048, 4096, 32)
        self.assertEqual(result, 0)

    def test_helper_function_get_optimizer_memory(self):
        """Test the _get_optimizer_memory helper function."""
        # Test with AdamW
        result = _get_optimizer_memory(7, "AdamW")
        expected = 8 * 7 * (10**9)  # 8x multiplier * 7B parameters * 10^9
        self.assertEqual(result, expected)

        # Test with SGD
        result = _get_optimizer_memory(7, "SGD")
        expected = 4 * 7 * (10**9)  # 4x multiplier * 7B parameters * 10^9
        self.assertEqual(result, expected)

        # Test with invalid optimizer
        result = _get_optimizer_memory(7, "InvalidOptimizer")
        self.assertEqual(result, 0)

    def test_helper_function_get_gradient_memory(self):
        """Test the _get_gradient_memory helper function."""
        # Test with valid inputs (note: precision is hardcoded to float32 in the function)
        result = _get_gradient_memory(7, "float16")  # precision param is ignored
        expected = 4 * 7 * (10**9)  # float32 (4 bytes) * 7B parameters * 10^9
        self.assertEqual(result, expected)

        # Test with zero model size
        result = _get_gradient_memory(0, "float16")
        self.assertEqual(result, 0)

    def test_memory_format_consistency(self):
        """Test that memory format is consistent across different calculations."""
        # Test small model for MB range
        result_small = calculate_inference_memory(
            model_size=1,  # 1B model
            precision="int8",  # 1 byte
            batch_size=1,
            sequence_length=512,
            hidden_size=1024,
            num_hidden_layers=12,
            num_attention_heads=8,
        )

        # Test large model for GB range
        result_large = calculate_inference_memory(
            model_size=70,  # 70B model
            precision="float32",  # 4 bytes
            batch_size=8,
            sequence_length=4096,
            hidden_size=8192,
            num_hidden_layers=80,
            num_attention_heads=64,
        )

        # Both should have proper format
        for result in [result_small, result_large]:
            for key, value in result.items():
                # Should either be empty string or have proper unit
                if value:
                    units = ["Bytes", "KB", "MB", "GB", "TB"]
                    has_unit = any(unit in value for unit in units)
                    self.assertTrue(has_unit or value == "", f"Invalid format: {value}")


if __name__ == "__main__":
    unittest.main()
