import pytest
from txt2stix import get_all_extractors, pattern, lookups



all_extractors = get_all_extractors()


@pytest.mark.parametrize(
    "extractor_name",
    [
        k
        for k, v in all_extractors.items()
        if k not in ["pattern_ipv6_address_only", "pattern_user_agent"]
    ],
)
def test_extractor(extractor_name):
    extractor = all_extractors[extractor_name]
    text_content = "===== [POSITIVE] ======\n{positives}\n===== [NEGATIVE] ======\n{negatives}".format(
        positives="  ".join(extractor.prompt_positive_examples),
        negatives="\n".join(extractor.prompt_negative_examples),
    )
    match extractor.type:
        case "pattern":
            extractor.load()
            out = pattern.extract_all([extractor], text_content)
            # assert False, f"{out} + {text_content}"
            outputs = {item["value"] for item in out}
            if outputs:
                assert outputs.isdisjoint(
                    extractor.prompt_negative_examples
                ), "some negative items extracted"
            assert outputs == set(
                extractor.prompt_positive_examples
            ), "some positive items not extracted"
        case "lookup":
            extractor.load()
            out = lookups.extract_all([extractor], text_content)
            # assert False, f"{out} + {text_content}"
            outputs = {item["value"] for item in out}
            if outputs:
                assert outputs.isdisjoint(
                    extractor.prompt_negative_examples
                ), "some negative items extracted"
            assert outputs == set(
                extractor.prompt_positive_examples
            ), "some positive items not extracted"
        case _:
            pass
