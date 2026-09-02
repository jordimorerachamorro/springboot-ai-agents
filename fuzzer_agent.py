import logging
import sys
from dataclasses import dataclass, field
from typing import List

import requests
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("security_fuzzer")

HTTP_TIMEOUT_SECONDS = 10
LLM_TIMEOUT_SECONDS = 60

llm = ChatOpenAI(model="gpt-4o", temperature=0.2, timeout=LLM_TIMEOUT_SECONDS)


@dataclass
class FuzzRun:
    swagger_url: str
    target_base_url: str
    endpoints_found: List[str] = field(default_factory=list)
    attack_plan: str = ""
    security_report: str = ""


class SwaggerFetchError(Exception):
    """Raised when the target's OpenAPI contract can't be retrieved or parsed."""


def fetch_endpoints(swagger_url: str) -> List[str]:
    """Download and parse the target's OpenAPI contract. Raises on failure — a
    connection/parse error must not silently become fake endpoint data."""
    logger.info("Downloading OpenAPI contract from %s", swagger_url)
    try:
        response = requests.get(swagger_url, timeout=HTTP_TIMEOUT_SECONDS)
        response.raise_for_status()
        swagger_data = response.json()
    except (requests.RequestException, ValueError) as exc:
        raise SwaggerFetchError(f"Could not fetch/parse OpenAPI contract from {swagger_url}: {exc}") from exc

    paths = list(swagger_data.get("paths", {}).keys())
    if not paths:
        raise SwaggerFetchError(f"OpenAPI contract at {swagger_url} contained no paths")

    logger.info("Found %d endpoint(s)", len(paths))
    return paths


def draft_attack_plan(paths: List[str]) -> str:
    logger.info("Drafting attack plan for %d endpoint(s)", len(paths))
    prompt = (
        "Act as a senior pentester. Analyze these routes of a Spring Boot microservice: "
        f"{paths}. Design a test plan to attempt to bypass security or corrupt data inputs."
    )
    ai_response = llm.invoke([SystemMessage(content=prompt)])
    return ai_response.content


def draft_security_report(attack_plan: str) -> str:
    logger.info("Drafting final security report")
    prompt = (
        "Based on this attack plan: "
        f"{attack_plan}, generate a final Markdown report detailing which endpoints "
        "should be monitored more closely in Spring Boot and which inputs to validate."
    )
    ai_response = llm.invoke([SystemMessage(content=prompt)])
    return ai_response.content


def run(swagger_url: str, target_base_url: str) -> FuzzRun:
    """Sequential two-step pipeline: fetch the contract, then draft a report.
    Deliberately not an agent loop — the step sequence is fixed and known upfront,
    so a fixed pipeline is simpler and more predictable than an agent framework."""
    result = FuzzRun(swagger_url=swagger_url, target_base_url=target_base_url)
    result.endpoints_found = fetch_endpoints(swagger_url)
    result.attack_plan = draft_attack_plan(result.endpoints_found)
    result.security_report = draft_security_report(result.attack_plan)
    return result


if __name__ == "__main__":
    # Make sure your Spring Boot service is running locally before running this.
    # By default, Springdoc exposes the JSON at: http://localhost:8080/v3/api-docs
    swagger_url = "http://localhost:8080/v3/api-docs"
    target_base_url = "http://localhost:8080"

    logger.info("Starting security report agent against %s", target_base_url)
    try:
        final_result = run(swagger_url, target_base_url)
    except SwaggerFetchError as exc:
        logger.error("Aborting: %s", exc)
        sys.exit(1)

    print("\n" + "=" * 40)
    print(" SECURITY REPORT")
    print("=" * 40)
    print(final_result.security_report)
