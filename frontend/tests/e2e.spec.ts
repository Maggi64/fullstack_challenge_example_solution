import { test, expect } from '@playwright/test';

test.describe('Countries Dashboard', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('http://localhost:5050'); // Adjust the URL to your local environment
  });

  test('should filter countries by name', async ({ page }) => {
    // Locate the countries overview panel
    const overviewPanel = page.locator('.p-panel:has-text("Countries Overview")');
    const searchInput = overviewPanel.locator('input[placeholder="Search by name"]');
    await searchInput.fill('Germany');

    // Check that the countries table is filtered accordingly
    const countryRows = overviewPanel.locator('.p-datatable-tbody tr');
    await expect(countryRows).toHaveCount(1);

    const countryName = await countryRows.first().locator('td').first().textContent();
    expect(countryName).toBe('Germany');
  });

  test('should toggle favorite status', async ({ page }) => {
    // Locate the countries overview panel
    const overviewPanel = page.locator('.p-panel:has-text("Countries Overview")');
    const firstFavoriteButton = overviewPanel.locator('.p-datatable-tbody tr').first().locator('button');
    const initialText = await firstFavoriteButton.textContent();
    
    await firstFavoriteButton.click();
    
    // Verify that the favorite status toggles
    const newText = await firstFavoriteButton.textContent();
    expect(newText).not.toBe(initialText);
  });
});
