from deepip.core.views.formating import Color


def test_color_fill():
    color_code = '30m'
    test_text = 'some text'

    colorful_text = Color.fill(test_text, color_code)

    assert (
        colorful_text == ''.join((Color.BORDER_START, color_code, test_text, Color.BORDER_END))
    ), 'formatted text should contain color code and correct borders'
