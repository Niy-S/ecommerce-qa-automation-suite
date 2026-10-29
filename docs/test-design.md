1. Generated an initial set of 35 test cases for https://www.saucedemo.com with an LLM (Claude, October 2026).

> You are a senior QA engineer. Generate test cases for the demo e-commerce site
> https://www.saucedemo.com covering these areas: login, product inventory and
> sorting, shopping cart, and checkout.
>
> Include positive, negative, boundary and edge cases. Output a table with columns:
> ID, Area, Scenario, Steps, Expected Result, Type (Positive/Negative/Edge/Boundary), Priority (High/Med/Low).
> Aim for around 30 test cases.

The AI produced a broad, well-structured set of 35 cases across login, inventory, cart and checkout, and most of its expected results matched the real site when I verified them manually. It was weaker on real behaviour: it assumed an empty cart would be blocked at checkout, but the site let me finish a $0 order, and it expected postal-code validation that doesn't exist. It also missed features entirely, such as the "Generate PDF order" button on the confirmation page. Reviewing each case against the live application surfaced six defects that the AI's expected results alone would never have caught. Next, I would automate the remaining backlog cases and add tests for the confirmed defects, marked as expected failures so they stay visible in the suite.