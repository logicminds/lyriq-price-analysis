// Auto-generated chart data for Cadillac Lyriq Dashboard
// Generated from CarGurus JSON data
// Do not edit manually - regenerate using extract_chart_data.py

// Location data for geographic distribution chart
const locationData = {
    'CA': { count: 82, avgPrice: 53484, trims: ['Sport 1', 'Luxury 1', 'Luxury 2'] },
    'TX': { count: 62, avgPrice: 44142, trims: ['Luxury 3', 'Luxury 1', 'Sport 3'] },
    'FL': { count: 52, avgPrice: 42474, trims: ['Sport 1', 'Luxury 1', 'Luxury 3'] },
    'OH': { count: 42, avgPrice: 44577, trims: ['Luxury 3', 'Sport 1', 'Luxury 1'] },
    'IL': { count: 32, avgPrice: 45617, trims: ['Luxury 3', 'Sport 1', 'Luxury 1'] },
    'NY': { count: 31, avgPrice: 49441, trims: ['Luxury 1', 'Sport 1', 'Luxury 3'] },
    'GA': { count: 31, avgPrice: 43973, trims: ['Sport 3', 'Sport 1', 'Luxury 1'] },
    'MD': { count: 30, avgPrice: 50799, trims: ['Luxury 1', 'Luxury 3', 'Sport 2'] },
    'PA': { count: 28, avgPrice: 44197, trims: ['Luxury 3', 'Sport 1', 'Luxury 1'] },
    'MO': { count: 22, avgPrice: 42501, trims: ['Luxury 3', 'Luxury 1', 'Sport 1'] },
    'MI': { count: 18, avgPrice: 44756, trims: ['Luxury 3', 'Luxury 1', 'Sport 1'] },
    'NC': { count: 17, avgPrice: 43528, trims: ['Luxury 3', 'Sport 2', 'Luxury 1'] },
    'WA': { count: 16, avgPrice: 45704, trims: ['Sport 1', 'Luxury 1', 'Sport 2'] },
    'NJ': { count: 14, avgPrice: 40613, trims: ['Luxury', 'Tech', 'Luxury 1'] },
    'AZ': { count: 13, avgPrice: 46646, trims: ['Luxury 3', 'Luxury 2', 'Sport 2'] },
    'MN': { count: 13, avgPrice: 43249, trims: ['Luxury 3', 'Luxury 1', 'Sport 1'] },
    'MA': { count: 13, avgPrice: 49590, trims: ['Luxury 3', 'Sport 1', 'Luxury 1'] },
    'VA': { count: 12, avgPrice: 45189, trims: ['Luxury 3', 'Luxury 1', 'Luxury'] },
    'IN': { count: 12, avgPrice: 44536, trims: ['Tech', 'Luxury 3', 'Luxury 1'] },
    'TN': { count: 12, avgPrice: 43130, trims: ['Luxury 3', 'Luxury 1', 'Sport 1'] },
    'WI': { count: 11, avgPrice: 46993, trims: ['Luxury 3', 'Sport 2'] },
    'CT': { count: 9, avgPrice: 45200, trims: ['Luxury 3', 'Luxury', 'Luxury 1'] },
    'NV': { count: 6, avgPrice: 43357, trims: ['Sport 1', 'Luxury', 'Sport 3'] },
    'KY': { count: 6, avgPrice: 42330, trims: ['Tech', 'Sport 1', 'Luxury 1'] },
    'OK': { count: 4, avgPrice: 39908, trims: ['Sport 1', 'Sport 3', 'Luxury 3'] },
    'AR': { count: 4, avgPrice: 44343, trims: ['Luxury 3'] },
    'RI': { count: 4, avgPrice: 46154, trims: ['Luxury 1', 'Luxury 3'] },
    'CO': { count: 4, avgPrice: 42568, trims: ['Sport 1', 'Tech', 'Luxury 3'] },
    'AL': { count: 3, avgPrice: 41332, trims: ['Tech', 'Luxury 1'] },
    'OR': { count: 3, avgPrice: 44990, trims: ['Luxury 3'] },
    'LA': { count: 3, avgPrice: 39664, trims: ['Tech', 'Luxury 1'] },
    'IA': { count: 2, avgPrice: 46316, trims: ['Luxury 3'] },
    'KS': { count: 2, avgPrice: 38982, trims: ['Luxury', 'Sport 1'] },
    'SC': { count: 2, avgPrice: 43743, trims: ['Luxury 1', 'Luxury 3'] },
    'NH': { count: 2, avgPrice: 44935, trims: ['Luxury 2', 'Luxury'] },
    'UT': { count: 2, avgPrice: 40412, trims: ['Sport 2', 'Luxury'] },
    'NM': { count: 1, avgPrice: 42997, trims: ['Luxury 2'] },
    'WV': { count: 1, avgPrice: 45966, trims: ['Luxury 3'] },
    'AK': { count: 1, avgPrice: 44649, trims: ['Sport 1'] },
    'MS': { count: 1, avgPrice: 43490, trims: ['Sport 1'] }
};

// Trim distribution data for stacked bar chart
const trimDistributionData = {
    trims: ['Luxury', 'Luxury 1', 'Luxury 2', 'Luxury 3', 'Sport 1', 'Sport 2', 'Sport 3', 'Tech', 'V-Series'],
    states: [
        { state: 'CA', total: 82, trims: [3, 24, 7, 4, 28, 7, 5, 4, 0] },
        { state: 'TX', total: 62, trims: [3, 11, 8, 16, 6, 4, 10, 4, 0] },
        { state: 'FL', total: 52, trims: [2, 13, 4, 9, 14, 1, 4, 5, 0] },
        { state: 'OH', total: 42, trims: [1, 7, 1, 18, 8, 2, 2, 3, 0] },
        { state: 'IL', total: 32, trims: [0, 6, 1, 11, 7, 4, 1, 2, 0] },
        { state: 'NY', total: 31, trims: [2, 9, 2, 6, 9, 0, 1, 2, 0] },
        { state: 'GA', total: 31, trims: [3, 5, 1, 2, 6, 1, 11, 2, 0] },
        { state: 'MD', total: 30, trims: [0, 10, 3, 9, 3, 4, 0, 1, 0] },
        { state: 'PA', total: 28, trims: [1, 5, 1, 8, 8, 0, 2, 3, 0] },
        { state: 'MO', total: 22, trims: [0, 5, 0, 11, 3, 0, 1, 2, 0] },
        { state: 'MI', total: 18, trims: [0, 5, 2, 7, 4, 0, 0, 0, 0] },
        { state: 'NC', total: 17, trims: [0, 2, 1, 8, 2, 3, 1, 0, 0] },
        { state: 'WA', total: 16, trims: [0, 4, 1, 0, 8, 3, 0, 0, 0] },
        { state: 'NJ', total: 14, trims: [4, 3, 1, 0, 3, 0, 0, 3, 0] },
        { state: 'AZ', total: 13, trims: [0, 0, 2, 3, 2, 2, 2, 2, 0] },
        { state: 'MN', total: 13, trims: [0, 3, 0, 8, 1, 0, 1, 0, 0] },
        { state: 'MA', total: 13, trims: [0, 2, 0, 7, 3, 0, 1, 0, 0] },
        { state: 'VA', total: 12, trims: [2, 2, 0, 4, 2, 0, 1, 0, 1] },
        { state: 'IN', total: 12, trims: [0, 3, 0, 3, 2, 1, 0, 3, 0] },
        { state: 'TN', total: 12, trims: [0, 3, 1, 4, 2, 0, 1, 1, 0] },
        { state: 'WI', total: 11, trims: [0, 0, 0, 10, 0, 1, 0, 0, 0] },
        { state: 'CT', total: 9, trims: [2, 2, 0, 5, 0, 0, 0, 0, 0] },
        { state: 'NV', total: 6, trims: [1, 1, 1, 0, 2, 0, 1, 0, 0] },
        { state: 'KY', total: 6, trims: [0, 1, 0, 1, 1, 0, 1, 2, 0] }
    ]
};

// Color palette for trim levels
const trimColors = {
    'Luxury': '#4ECDC4',
    'Luxury 1': '#45B7D1',
    'Luxury 2': '#96CEB4',
    'Luxury 3': '#FFEAA7',
    'Sport 1': '#DDA0DD',
    'Sport 2': '#98D8C8',
    'Sport 3': '#F7DC6F',
    'Tech': '#BB8FCE',
    'V-Series': '#FF6B6B'
};

// Usage instructions:
// 1. Copy the locationData object to replace the locationData in index.html
// 2. Copy the trimDistributionData object to replace the trimDistributionData in index.html
// 3. Copy the trimColors object to replace the trimColors in index.html
// 4. Update chart titles with current date if needed