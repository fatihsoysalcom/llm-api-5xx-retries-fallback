import time
import random

# --- Configuration Parameters ---
MAX_RETRIES = 3  # Maximum number of retry attempts for the LLM API call
INITIAL_BACKOFF_DELAY_SECONDS = 1  # Initial delay before the first retry
LLM_API_ERROR_RATE = 0.7  # Probability (0.0 to 1.0) of the simulated LLM API returning a 5xx error

# --- Simulated LLM API Call ---
def call_llm_api(prompt: str) -> dict:
    """
    Simulates an API call to an LLM, which might return a 5xx error.
    """
    print(f"  [API Call] Attempting to call LLM API with prompt: '{prompt}'...")
    time.sleep(0.3)  # Simulate network latency

    # Simulate a 5xx error based on the configured error rate
    if random.random() < LLM_API_ERROR_RATE:
        print("  [API Call] LLM API returned a 5xx error (simulated).")
        return {"status": 500, "message": "Internal Server Error (simulated)"}
    else:
        print("  [API Call] LLM API call successful (simulated).")
        return {"status": 200, "response": f"LLM says: '{prompt}' is a fascinating topic!"}

# --- Fallback Function ---
def get_fallback_response(prompt: str) -> str:
    """
    Provides a predefined or simpler response when the primary LLM API fails.
    """
    print(f"  [Fallback] Generating a fallback response for prompt: '{prompt}'...")
    # In a real application, this could be a cached response, a simpler rule-based answer,
    # or a call to a less sophisticated, more reliable local model.
    return f"FALLBACK: Due to API issues, here's a basic answer for '{prompt}'."

# --- Main Logic with Retries and Fallback ---
def get_llm_response_with_resilience(prompt: str) -> str:
    """
    Attempts to get a response from the LLM API with retry logic (exponential backoff)
    and falls back to a default response if all retries fail.
    """
    current_retries = 0
    current_delay = INITIAL_BACKOFF_DELAY_SECONDS

    print(f"\n--- Processing prompt: '{prompt}' ---")

    while current_retries < MAX_RETRIES:
        print(f"  [Retry] Attempt {current_retries + 1}/{MAX_RETRIES}...")
        api_response = call_llm_api(prompt)

        # Check if the API call was successful (status 200)
        if api_response["status"] == 200:
            print("  [Success] Successfully received LLM response.")
            return api_response["response"]
        # Check for 5xx errors (server-side errors) that warrant a retry
        elif 500 <= api_response["status"] < 600:
            print(f"  [Error] Received 5xx error. Retrying in {current_delay:.1f} seconds...")
            time.sleep(current_delay)
            current_delay *= 2  # Exponential backoff: double the delay for the next retry
            current_retries += 1
        else:
            # For other types of errors (e.g., 4xx client errors), do not retry
            print(f"  [Error] Received unexpected status {api_response['status']}. Not retrying, falling back.")
            return get_fallback_response(prompt)

    # If all retry attempts fail, execute the fallback strategy
    print(f"  [Failure] All {MAX_RETRIES} retry attempts failed for prompt: '{prompt}'.")
    return get_fallback_response(prompt)

# --- Example Usage ---
if __name__ == "__main__":
    # Scenario 1: Demonstrates a successful call, potentially after some retries
    print("\n===== Scenario 1: Successful call (may require retries) =====")
    final_response_1 = get_llm_response_with_resilience("What is the capital of France?")
    print(f"Final Result 1: {final_response_1}")

    # Scenario 2: Demonstrates all retries failing and the fallback being used
    print("\n===== Scenario 2: All retries fail, fallback is used =====")
    # Temporarily increase error rate to ensure fallback is hit for demonstration
    original_error_rate = LLM_API_ERROR_RATE
    LLM_API_ERROR_RATE = 0.95  # Make errors very likely for this scenario
    final_response_2 = get_llm_response_with_resilience("Tell me a short story about a brave knight.")
    print(f"Final Result 2: {final_response_2}")
    LLM_API_ERROR_RATE = original_error_rate  # Reset error rate for subsequent calls

    # Scenario 3: Another attempt with the original error rate
    print("\n===== Scenario 3: Another attempt with original error rate =====")
    final_response_3 = get_llm_response_with_resilience("Explain quantum entanglement simply.")
    print(f"Final Result 3: {final_response_3}")
