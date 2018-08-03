import {
    Selector,
    ClientFunction,
    t
} from 'testcafe';

// install TestCafe as instructed at https://devexpress.github.io/testcafe/ then run with "testcafe chrome /path-to-test-file.js"

// page-model section (this should be in a separate file then import here, but for illustration, I put here for easier checking)
var password = Selector('#Password'),
    submit = Selector('.submit_button'),
    required_fields = Selector('.q.required'),
    first_name = Selector('#RESULT_TextField-1'),
    last_name = Selector('#RESULT_TextField-2'),
    street = Selector('#RESULT_TextField-3'),
    address2 = Selector('#RESULT_TextField-4'),
    city = Selector('#RESULT_TextField-5'),
    state_select = Selector('#RESULT_RadioButton-6'),
    state_option = Selector(state_select).find('option'),
    zip = Selector('#RESULT_TextField-7'),
    phone = Selector('#RESULT_TextField-8'),
    email = Selector('#RESULT_TextField-9'),
    date_text = Selector('#RESULT_TextField-10'),
    date_icon = Selector('img[alt="calendar"]'),
    year_select = Selector('.ui-datepicker-year'),
    year_option = Selector(year_select).find('option'),
    day = Selector('a[class="ui-state-default"]');

async function bypass() {
    await t
        .typeText(password, 'secret')
        .click(submit);
};

const getPageUrl = ClientFunction(() => document.location.href);

// test case section
fixture('Test form')
    .page('https://fs28.formsite.com/ecnvietnam/form1/index.html') // start page
    .beforeEach(async t => {
        await bypass()
    }); // input password to access form

test('Submit all empty data', async t => {
    var count = await required_fields.count; // count required fields

    await t
        .click(submit)
        .expect(required_fields.count).eql(8);

    for (let i = 0; i < count; i++) {
        // console.log(i)
        await t
            .expect(required_fields.nth(i).find('.invalid_message').textContent).eql('Response required')
    }
});

test('Submit all correct data', async t => {
    await t
        .typeText(first_name, 'hung')
        .typeText(last_name, 'tran')
        .typeText(street, 'test')
        .typeText(address2, 'test2')
        .typeText(city, 'hcm')
        .click(state_select)
        .click(state_option.withAttribute('value', 'Radio-1'))
        .typeText(zip, '12345')
        .typeText(phone, '214453454353')
        .typeText(email, 'trannguyenhung011086@gmail.com')
        .click(date_icon)
        .click(year_select)
        .click(year_option.withText('1986'))
        .click(day.withText('16'))
        .click(submit)
        .expect(getPageUrl()).contains('showSuccessPage')
});

test('Submit wrong phone format', async t => {
    await t
        .typeText(phone, 'abcdef')
        .click(submit)
        .expect(phone.parent(0).find('.invalid_message').textContent).eql('Invalid phone number')
});

test('Submit wrong email format', async t => {
    await t
        .typeText(email, 'abcdef@adb')
        .click(submit)
        .expect(email.parent(0).find('.invalid_message').textContent).eql('Invalid email address')
});

test('Submit wrong date format', async t => {
    await t
        .typeText(date_text, '453534')
        .click(submit)
        .expect(date_text.parent(0).find('.invalid_message').textContent).eql('Invalid date')
});